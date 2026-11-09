"""Project 07: one-pass reproducible statistical export and quality checks.

Run from any directory using the project's Python interpreter:
    python python/finalize_project.py

Loads the unchanged ISO-formatted synthetic source CSV. This script deliberately
never edits data/support_tickets.csv, the notebook, or the executive report.
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.oneway import anova_oneway

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'support_tickets.csv'
OUT = ROOT / 'output' / 'statistical_results.csv'
FIG_DIR = ROOT / 'output' / 'figures'


def require(condition, message):
    if not bool(condition):
        raise ValueError(message)


def approx(actual, reference, tolerance, label):
    require(np.isclose(actual, reference, atol=tolerance, rtol=0),
            f'{label}: expected approximately {reference}, found {actual}')


def main():
    require(DATA.is_file(), f'Missing source dataset: {DATA}')
    # Read the raw source first: never rely on ambiguous day/month guessing.
    df = pd.read_csv(DATA, dtype={'ticket_date': 'string'})
    required = {
        'ticket_id', 'ticket_date', 'intervention_period', 'agent_id', 'team',
        'ticket_category', 'ticket_priority', 'ticket_complexity',
        'response_time_minutes', 'resolution_time_minutes', 'csat_rating',
        'sla_target_minutes', 'training_completed'
    }
    require(required.issubset(df.columns), f'Missing columns: {required - set(df.columns)}')
    try:
        df['ticket_date'] = pd.to_datetime(df['ticket_date'], format='%Y-%m-%d', errors='raise')
    except (ValueError, TypeError) as exc:
        raise ValueError('ticket_date must use YYYY-MM-DD in data/support_tickets.csv') from exc

    periods = ['Before', 'After']
    dates = df['ticket_date'].dt.normalize()
    is_before = df['intervention_period'].eq('Before')
    is_after = df['intervention_period'].eq('After')
    date_ok = (
        (is_before & dates.between(pd.Timestamp('2026-07-01'), pd.Timestamp('2026-08-14'))) |
        (is_after & dates.between(pd.Timestamp('2026-08-15'), pd.Timestamp('2026-09-28')))
    )
    coverage = df.groupby(['agent_id', 'intervention_period']).size().unstack(fill_value=0)
    matched = coverage.get('Before', pd.Series(0, index=coverage.index)).ge(25) & coverage.get('After', pd.Series(0, index=coverage.index)).ge(25)
    missing_identifiers = df[['agent_id','team','ticket_category']].isna().any().any() or any(
        df[c].astype('string').str.strip().eq('').any() for c in ['agent_id','team','ticket_category']
    )
    checks = {
        'Unique and present ticket IDs': df['ticket_id'].notna().all() and df['ticket_id'].is_unique and df['ticket_id'].astype('string').str.strip().ne('').all(),
        'No duplicate records': not df.duplicated().any(),
        'Required identifiers populated': not missing_identifiers,
        'Valid intervention periods': set(df['intervention_period']) == set(periods),
        'Valid teams, priorities and complexity': (
            df['team'].isin(['Billing','General','Technical']).all() and
            df['ticket_priority'].isin(['Low','Medium','High']).all() and
            df['ticket_complexity'].isin(['Simple','Moderate','Complex']).all()),
        'Valid response and resolution times': (
            df['response_time_minutes'].gt(0).all() and
            df['resolution_time_minutes'].ge(df['response_time_minutes']).all()),
        'Valid CSAT ratings': (df['csat_rating'].isna() | df['csat_rating'].isin([1,2,3,4,5])).all(),
        'Correct SLA targets': df['sla_target_minutes'].eq(df['ticket_priority'].map({'High':10,'Medium':20,'Low':30})).all(),
        'Consistent agent-team assignments': df.groupby('agent_id')['team'].nunique().eq(1).all(),
        'Correct training flags': df['training_completed'].eq(is_after).all(),
        'Correct reporting dates': date_ok.all(),
        'Sufficient tickets per agent': matched.all() and matched.size == 45,
    }
    print('=== CONSOLIDATED DATA AUDIT ===')
    for label, passed in checks.items():
        print(f'{"PASS" if passed else "FAIL"}: {label}')
    require(all(checks.values()), 'Audit failed: do not export results.')
    require(len(df) == 4150, f'Expected 4150 simulated tickets; found {len(df)}')
    require(df['agent_id'].nunique() == 45, 'Expected 45 distinct agents')

    df['sla_met'] = df['response_time_minutes'].le(df['sla_target_minutes'])
    df['satisfied'] = df['csat_rating'].ge(4)
    df['has_rating'] = df['csat_rating'].notna()
    rows = []

    def add(section, metric, segment, value, unit='', definition=''):
        if value is None or pd.isna(value):
            return
        rows.append(dict(section=section, metric=metric, segment=segment,
                         value=round(float(value), 8), unit=unit, definition=definition))

    # Period-specific ticket-weighted KPIs.
    for period in periods:
        x = df.loc[df['intervention_period'].eq(period)]
        rated = x.loc[x['has_rating']]
        require(len(rated) > 0, 'No ratings for period ' + period)
        metrics = [
            ('tickets', len(x), 'tickets', 'All support tickets'),
            ('agents', x['agent_id'].nunique(), 'agents', 'Distinct active agents'),
            ('mean_response', x['response_time_minutes'].mean(), 'minutes', 'Ticket-weighted first-response mean'),
            ('median_response', x['response_time_minutes'].median(), 'minutes', 'Ticket-level first-response median'),
            ('mean_resolution', x['resolution_time_minutes'].mean(), 'minutes', 'Ticket-weighted resolution mean'),
            ('median_resolution', x['resolution_time_minutes'].median(), 'minutes', 'Ticket-level resolution median'),
            ('sla_met_tickets', x['sla_met'].sum(), 'tickets', 'Tickets meeting priority-specific response SLA'),
            ('sla_pct', 100*x['sla_met'].mean(), '%', 'SLA-met tickets / all tickets x100'),
            ('csat_responses', len(rated), 'tickets', 'Tickets with recorded CSAT'),
            ('csat_response_pct', 100*x['has_rating'].mean(), '%', 'Rated tickets / all tickets x100'),
            ('mean_csat', rated['csat_rating'].mean(), 'rating/5', 'Mean among rated tickets'),
            ('satisfied_ratings', x['satisfied'].sum(), 'tickets', 'Rated CSAT 4 or 5'),
            ('satisfied_pct', 100*x['satisfied'].sum()/len(rated), '%', 'CSAT 4/5 responses / all CSAT responses x100'),
            ('high_priority_pct', 100*x['ticket_priority'].eq('High').mean(), '%', 'High-priority tickets / all tickets x100'),
            ('complex_pct', 100*x['ticket_complexity'].eq('Complex').mean(), '%', 'Complex tickets / all tickets x100'),
        ]
        for metric, value, unit, desc in metrics:
            add('overall_kpi', metric, period, value, unit, desc)

    # Period-by-team operational stats.
    for (team,period), x in df.groupby(['team', 'intervention_period']):
        rated = x.loc[x['has_rating']]
        segment = f'{team} | {period}'
        for metric,value,unit,desc in [
            ('tickets',len(x),'tickets','Ticket count'),
            ('mean_response',x['response_time_minutes'].mean(),'minutes','Ticket-weighted mean'),
            ('mean_resolution',x['resolution_time_minutes'].mean(),'minutes','Ticket-weighted mean'),
            ('sla_pct',100*x['sla_met'].mean(),'%','SLA-met / all tickets x100'),
            ('mean_csat',rated['csat_rating'].mean(),'rating/5','Mean rated CSAT'),
            ('csat_response_pct',100*len(rated)/len(x),'%','Rated / all tickets x100'),
            ('satisfied_pct',100*rated['satisfied'].mean(),'%','CSAT 4/5 / rated tickets x100'),
        ]:
            add('team_kpi',metric,segment,value,unit,desc)

    for dimension in ('ticket_priority','ticket_complexity'):
        for (period, segment), x in df.groupby(['intervention_period',dimension]):
            label = f'{period} | {segment}'
            for metric,val,unit in [
                ('tickets',len(x),'tickets'),
                ('mean_response',x['response_time_minutes'].mean(),'minutes'),
                ('mean_resolution',x['resolution_time_minutes'].mean(),'minutes'),
                ('sla_pct',100*x['sla_met'].mean(),'%')]:
                add(f'{dimension}_kpi',metric,label,val,unit)

    paired = (df.groupby(['agent_id','team','intervention_period'])['response_time_minutes']
                .mean().unstack('intervention_period'))
    require(len(paired) == 45 and paired[periods].notna().all().all(), 'Agent pairing failed')
    paired['improvement_min'] = paired['Before'] - paired['After']
    d = paired['improvement_min'].to_numpy(dtype=float)
    n = len(d); mean_d = d.mean(); sd = d.std(ddof=1); se = sd/np.sqrt(n)
    primary = stats.ttest_rel(paired['Before'],paired['After'])
    manual_t = mean_d/se
    require(np.isclose(primary.statistic, manual_t), 'Manual and SciPy paired t disagreement')
    tc = stats.t.ppf(.975, n-1)
    ci = (mean_d-tc*se, mean_d+tc*se)
    shapiro = stats.shapiro(d)
    for metric, value, unit in [
        ('matched_agents', n, 'agents'),('agent_mean_before',paired['Before'].mean(),'minutes'),
        ('agent_mean_after',paired['After'].mean(),'minutes'),('mean_improvement',mean_d,'minutes'),
        ('median_improvement',np.median(d),'minutes'),('sd_improvement',sd,'minutes'),
        ('se_improvement',se,'minutes'),('t_statistic',primary.statistic,'t'),
        ('degrees_of_freedom',n-1,'df'),('p_value_two_sided',primary.pvalue,'p'),
        ('ci95_lower',ci[0],'minutes'),('ci95_upper',ci[1],'minutes'),
        ('cohens_dz',mean_d/sd,'standardized'),
        ('shapiro_w',shapiro.statistic,'W'),('shapiro_p',shapiro.pvalue,'p'),
        ('agents_improved',(d>0).sum(),'agents'),('agents_deteriorated',(d<0).sum(),'agents')]:
        add('paired_t_test',metric,'all_45_agents',value,unit)
    approx(mean_d,.8186,.0001,'Mean paired improvement')
    approx(primary.statistic,1.8757,.0001,'Paired t')
    approx(primary.pvalue,.0673,.0001,'Paired p')
    approx(ci[0],-.0610,.0001,'Paired CI lower')

    # Classical ANOVA with manual SS and Welch comparison.
    groups = {name:x['improvement_min'].to_numpy(dtype=float)
              for name,x in paired.reset_index().groupby('team')}
    require(set(groups)=={'Billing','General','Technical'}, 'Unexpected team groups')
    f,p = stats.f_oneway(*groups.values())
    grand = np.concatenate(list(groups.values())).mean()
    ss_between = sum(len(x)*(x.mean()-grand)**2 for x in groups.values())
    ss_within = sum(((x-x.mean())**2).sum() for x in groups.values())
    df_between = len(groups)-1
    df_within = n-len(groups)
    require(np.isclose(f,(ss_between/df_between)/(ss_within/df_within)), 'Manual ANOVA mismatch')
    welch = anova_oneway(list(groups.values()),use_var='unequal')
    lev = stats.levene(*groups.values(),center='median')
    for team,x in groups.items():
        add('team_agent_improvement','agents',team,len(x),'agents')
        add('team_agent_improvement','mean_improvement',team,x.mean(),'minutes')
        add('team_agent_improvement','shapiro_p',team,stats.shapiro(x).pvalue,'p')
    for metric,value,unit in [
        ('ss_between',ss_between,'min^2'),('ss_within',ss_within,'min^2'),
        ('ms_between',ss_between/df_between,'min^2'),('ms_within',ss_within/df_within,'min^2'),
        ('df_between',df_between,'df'),('df_within',df_within,'df'),
        ('classical_f',f,'F'),('classical_p',p,'p'),
        ('welch_f',welch.statistic,'F'),('welch_p',welch.pvalue,'p'),
        ('eta_squared',ss_between/(ss_between+ss_within),'proportion'),
        ('levene_p',lev.pvalue,'p')]:
        add('anova',metric,'all_45_agents',value,unit)
    approx(f,1.8256,.0001,'ANOVA F')
    approx(p,.1737,.0001,'ANOVA p')
    approx(welch.pvalue,.2009,.0001,'Welch p')

    # AGT028 exploratory exclusion only; source dataset and primary analysis unchanged.
    require('AGT028' in paired.index.get_level_values('agent_id'), 'Missing AGT028')
    without = paired.loc[paired.index.get_level_values('agent_id')!='AGT028']
    ds = without['improvement_min'].to_numpy(dtype=float)
    t_s = stats.ttest_1samp(ds, 0)
    se_s = ds.std(ddof=1)/np.sqrt(len(ds))
    tcrit_s = stats.t.ppf(.975,len(ds)-1)
    for metric,value,unit in [
        ('agents',len(ds),'agents'),('mean_improvement',ds.mean(),'minutes'),
        ('t_statistic',t_s.statistic,'t'),('p_value_two_sided',t_s.pvalue,'p'),
        ('ci95_lower',ds.mean()-tcrit_s*se_s,'minutes'),
        ('ci95_upper',ds.mean()+tcrit_s*se_s,'minutes')]:
        add('sensitivity_paired',metric,'exclude_AGT028_exploratory',value,unit)
    gs = {name:x['improvement_min'].to_numpy(dtype=float)
          for name,x in without.reset_index().groupby('team')}
    fs,ps = stats.f_oneway(*gs.values())
    ws = anova_oneway(list(gs.values()),use_var='unequal')
    for metric,value,unit in [
        ('classical_f',fs,'F'),('classical_p',ps,'p'),
        ('welch_f',ws.statistic,'F'),('welch_p',ws.pvalue,'p'),
        ('technical_mean_improvement',gs['Technical'].mean(),'minutes')]:
        add('sensitivity_anova',metric,'exclude_AGT028_exploratory',value,unit)
    approx(t_s.pvalue,.0054,.0001,'Sensitivity paired p')
    approx(ps,.2995,.0001,'Sensitivity ANOVA p')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(OUT,index=False)
    figures = [
        '01_response_time_comparison.png','02_response_time_distribution.png',
        '03_agent_level_improvements.png','04_team_level_improvements.png',
        '05_customer_experience_guardrails.png',
    ]
    missing_figures = [f for f in figures if not (FIG_DIR/f).is_file()]
    missing_docs = [str(p.relative_to(ROOT)) for p in [
        ROOT/'README.md',ROOT/'docs'/'business_requirements.md',
        ROOT/'docs'/'executive_decision_report.md',
        ROOT/'notebooks'/'support_training_analysis.ipynb'
    ] if not p.is_file()]

    print('\n=== NUMERIC RECONCILIATION ===')
    print(f'Rows: {len(df)} | agents: {n} | 12/12 audit PASS')
    print(f'Paired t({n-1}) = {primary.statistic:.4f}; p = {primary.pvalue:.4f}; '
          f'mean improvement = {mean_d:.4f} min; CI [{ci[0]:.4f}, {ci[1]:.4f}]')
    print(f'Classical ANOVA F({df_between},{df_within}) = {f:.4f}; p = {p:.4f}')
    print(f'Welch ANOVA F = {welch.statistic:.4f}; p = {welch.pvalue:.4f}')
    print(f'Statistical export saved: {OUT.relative_to(ROOT)} ({len(rows)} metrics)')
    if missing_figures:
        print('PENDING — Missing plot files:', ', '.join(missing_figures))
    else:
        print('PASS — All five figures present')
    if missing_docs:
        print('PENDING — Missing required project files:', ', '.join(missing_docs))
    else:
        print('PASS — README, BRD, executive report, and notebook present')
    if missing_figures or missing_docs:
        print('ACTION: Resolve missing files before GitHub publication.')
        sys.exit(2)
    print('PASS — Phase 5 quantitative and file-presence checks passed')
    print('NEXT — In VS Code: Restart Kernel and Run All notebook cells; inspect outputs.')


if __name__ == '__main__':
    main()
