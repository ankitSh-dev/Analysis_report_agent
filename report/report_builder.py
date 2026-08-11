"""
report_builder.py

Main Report Builder.
Responsible only for generating a structured report.
"""

from analysis.schemas import AnalysisResult

from report.prompts import (
    SYSTEM_PROMPT,
    REPORT_PROMPT,
)

from report.llm import ReportLLMService

from report.schemas import (
    LLMReportResponse,
)


class ReportBuilder:
    """
    Builds the logical report from the AnalysisResult.
    """

    def __init__(self):

        self.llm = ReportLLMService()

    # =====================================================

    def build_report(
        self,
        analysis: AnalysisResult,
    ) -> LLMReportResponse:
        """
        Generate a structured report.
        """

        prompt = self._build_prompt(
            analysis
        )

        return self.llm.generate_report(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
        )

    # =====================================================

    def _build_prompt(
        self,
        analysis: AnalysisResult,
    ) -> str:
        """
        Convert AnalysisResult into a report prompt.
        """

        return REPORT_PROMPT.format(
            analysis=analysis.model_dump_json(
                indent=2
            )
        )