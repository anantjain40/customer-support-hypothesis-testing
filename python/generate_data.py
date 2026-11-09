"""Generate one reproducible synthetic before/after customer-support ticket CSV.

Run from the repository root:
    python python/generate_data.py

All values are simulated, not observations from a real support company.
Never adjust the seed or training effects merely to obtain significant tests.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 20260707
OUTPUT_PATH = Path(__file__).resolve().parents[1] / "data" / "support_tickets.csv"

# The before and after windows each contain 45 days. There is no control group.
PERIODS = (
    ("Before", date(2026, 7, 1), 2_050),
    ("After", date(2026, 8, 15), 2_100),
)
TEAMS = ("Billing", "Technical", "General")
AGENTS_PER_TEAM = 15
MIN_TICKETS_PER_AGENT_PER_PERIOD = 25

# These are simulation assumptions, not measured effect estimates.
TEAM_BASE_MEAN_MINUTES = {"Billing": 15.0, "Technical": 16.5, "General": 11.5}
TEAM_MEAN_FRACTIONAL_TRAINING_EFFECT = {
    "Billing": 0.15, "Technical": 0.065, "General": 0.10
}
TEAM_RESOLUTION_SCALE = {"Billing": 38.0, "Technical": 53.0, "General": 31.0}
CATEGORIES = {
    "Billing": ("Refund", "Invoice", "Payment Failure", "Subscription"),
    "Technical": ("Login", "Application Error", "Performance", "Integration"),
    "General": ("Account Update", "Order Status", "Product Inquiry", "Policy"),
}
PRIORITY_MULTIPLIER = {"High": 0.76, "Medium": 1.00, "Low": 1.24}
COMPLEXITY_MULTIPLIER = {"Simple": 0.82, "Moderate": 1.00, "Complex": 1.35}
SLA_TARGET_MINUTES = {"High": 10, "Medium": 20, "Low": 30}


def allocate_agent_tickets(rng: np.random.Generator, total: int, weights: np.ndarray) -> np.ndarray:
    """Ensure sufficient pre/post observations for *every* agent."""
    minimum = len(weights) * MIN_TICKETS_PER_AGENT_PER_PERIOD
    if total < minimum:
        raise ValueError("Total tickets must exceed the minimum agent coverage.")
    return MIN_TICKETS_PER_AGENT_PER_PERIOD + rng.multinomial(total - minimum, weights / weights.sum())


def generate() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    agents = [
        (f"AGT{team_idx * AGENTS_PER_TEAM + i + 1:03d}", team)
        for team_idx, team in enumerate(TEAMS)
        for i in range(AGENTS_PER_TEAM)
    ]
    agent_weights = rng.uniform(0.80, 1.30, size=len(agents))

    # Persistent agent traits create correlation between tickets handled by the same agent.
    agent_speed_factor = rng.lognormal(mean=0.0, sigma=0.15, size=len(agents))
    # Individual responses to training vary; some agents do not improve or deteriorate.
    agent_training_effect = np.array(
        [rng.normal(TEAM_MEAN_FRACTIONAL_TRAINING_EFFECT[team], 0.115) for _, team in agents]
    )
    agent_training_effect = np.clip(agent_training_effect, -0.25, 0.38)

    rows: list[dict[str, object]] = []
    ticket_number = 1
    for period, start_date, ticket_count in PERIODS:
        agent_counts = allocate_agent_tickets(rng, ticket_count, agent_weights)
        for agent_index, ((agent_id, team), count) in enumerate(zip(agents, agent_counts)):
            for _ in range(int(count)):
                priority = str(
                    rng.choice(
                        ("High", "Medium", "Low"),
                        p=(0.22, 0.48, 0.30) if period == "Before" else (0.27, 0.47, 0.26),
                    )
                )
                complexity = str(
                    rng.choice(
                        ("Simple", "Moderate", "Complex"),
                        p=(0.35, 0.43, 0.22) if period == "Before" else (0.31, 0.41, 0.28),
                    )
                )
                category = str(rng.choice(CATEGORIES[team]))

                base_expected_response = (
                    TEAM_BASE_MEAN_MINUTES[team]
                    * agent_speed_factor[agent_index]
                    * PRIORITY_MULTIPLIER[priority]
                    * COMPLEXITY_MULTIPLIER[complexity]
                )
                period_factor = (
                    max(0.55, 1.0 - agent_training_effect[agent_index])
                    if period == "After"
                    else 1.0
                )
                # Right-skewed, strictly positive response times; sigma adds ticket variability.
                expected_response = base_expected_response * period_factor
                sigma = 0.46
                response_minutes = float(
                    np.clip(
                        rng.lognormal(np.log(expected_response) - sigma**2 / 2, sigma),
                        0.5,
                        180.0,
                    )
                )
                resolution_work = rng.gamma(
                    shape=2.7,
                    scale=TEAM_RESOLUTION_SCALE[team] * COMPLEXITY_MULTIPLIER[complexity],
                )
                resolution_minutes = response_minutes + float(resolution_work) + 1.0
                sla_target = SLA_TARGET_MINUTES[priority]
                meets_sla = response_minutes <= sla_target

                # Missing CSAT is survey nonresponse, not a one-star rating.
                response_probability = 0.79 if period == "Before" else 0.75
                if rng.random() < response_probability:
                    quality_center = (
                        4.15
                        + (0.10 if period == "After" else 0.0)
                        - (0.48 if not meets_sla else 0.0)
                        - (0.18 if complexity == "Complex" else 0.0)
                        - (0.16 if resolution_minutes > 270 else 0.0)
                    )
                    csat_rating: int | None = int(np.clip(np.rint(rng.normal(quality_center, 0.85)), 1, 5))
                else:
                    csat_rating = None

                ticket_day = start_date + timedelta(days=int(rng.integers(0, 45)))
                rows.append(
                    {
                        "ticket_id": f"TKT{ticket_number:06d}",
                        "ticket_date": ticket_day.isoformat(),
                        "intervention_period": period,
                        "agent_id": agent_id,
                        "team": team,
                        "ticket_category": category,
                        "ticket_priority": priority,
                        "ticket_complexity": complexity,
                        "response_time_minutes": round(response_minutes, 2),
                        "resolution_time_minutes": round(resolution_minutes, 2),
                        "csat_rating": csat_rating,
                        "sla_target_minutes": sla_target,
                        "training_completed": period == "After",
                    }
                )
                ticket_number += 1

    df = pd.DataFrame(rows)
    # A fixed permutation prevents the file from being sorted by agent / period.
    df = df.iloc[rng.permutation(len(df))].reset_index(drop=True)
    return df


def main() -> None:
    tickets = generate()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    tickets.to_csv(OUTPUT_PATH, index=False)
    matched = tickets.groupby("agent_id")["intervention_period"].nunique().eq(2).sum()
    print(f"Wrote {OUTPUT_PATH}")
    print(f"Tickets: {len(tickets):,} | Agents: {tickets.agent_id.nunique()} | Matched: {matched}")
    print("Synthetic data only. Never claim real-world training effectiveness.")


if __name__ == "__main__":
    main()
