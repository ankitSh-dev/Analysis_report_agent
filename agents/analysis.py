"""
analysis.py

Entry point for the Analysis Agent.
"""

from typing import Optional

from analysis.analyzer import AnalysisAgent

from analysis.schemas import (
    ExecutionResult,
    MonitoringResult,
    SecurityResult,
    AnalysisResult,
)


class AnalysisWorkflow:
    """
    Main Analysis Agent.

    Responsible for orchestrating the complete
    Performance Analysis workflow.

    This is the public entry point that should be
    used by the Team Orchestrator.
    """

    def __init__(self):

        self.analysis_agent = AnalysisAgent()

    # =====================================================

    def analyze(
        self,
        execution: Optional[ExecutionResult] = None,
        monitoring: Optional[MonitoringResult] = None,
        security: Optional[SecurityResult] = None,
    ) -> AnalysisResult:
        """
        Execute the complete Analysis Agent.

        Inputs:
            - ExecutionResult (optional)
            - MonitoringResult (optional)
            - SecurityResult (optional)

        Any combination of the three inputs can be provided.

        Returns:
            AnalysisResult
        """

        return self.analysis_agent.analyze(

            execution=execution,

            monitoring=monitoring,

            security=security,

        )