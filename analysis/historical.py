"""
historical.py

Historical execution comparison engine.
"""

from typing import List

import pandas as pd

from analysis.schemas import (
    ExecutionResult,
    HistoricalIncident,
    HistoricalSearchResult,
)
from data.loader import load_dataset


class HistoricalComparator:
    """
    Compare current execution with historical executions.
    """

    def find_similar(
        self,
        execution: ExecutionResult,
        top_k: int = 5,
    ) -> HistoricalSearchResult:
        """
        Return top similar historical executions.
        """

        df = load_dataset()

        # -----------------------------------------
        # Filter by Scenario
        # -----------------------------------------

        scenario_df = df[
            df["Scenario"] == execution.scenario
        ].copy()

        if scenario_df.empty:
            return HistoricalSearchResult(
                total_matches=0,
                matches=[],
            )

        # -----------------------------------------
        # Similarity Score
        # -----------------------------------------

        scenario_df["similarity"] = (
            abs(
                scenario_df["Response Time (ms)"]
                - execution.avg_response_time
            )
        )

        scenario_df = scenario_df.sort_values(
            by="similarity"
        )

        top_matches = scenario_df.head(top_k)

        incidents: List[HistoricalIncident] = []

        for _, row in top_matches.iterrows():

            similarity = (
                1
                - (
                    row["similarity"]
                    / max(
                        execution.avg_response_time,
                        1,
                    )
                )
            )

            similarity = max(
                0,
                round(similarity, 2),
            )

            incidents.append(
                HistoricalIncident(
                    job_id=row["Job ID"],
                    scenario=row["Scenario"],
                    bottleneck=row["Bottleneck"],
                    root_cause=row["Bottleneck"],
                    recommendation=row["Recommendation"],
                    similarity_score=similarity,
                )
            )

        return HistoricalSearchResult(
            total_matches=len(incidents),
            matches=incidents,
        )