"""
report.py

Entry point for the Report Agent.
"""

from pathlib import Path

from analysis.schemas import AnalysisResult

from report.report_builder import ReportBuilder
from report.pdf_generator import PDFGenerator
from report.html_generator import HTMLGenerator
from report.json_generator import JSONGenerator

from report.schemas import (
    ReportAgentResponse,
    GeneratedReports,
)


class ReportAgent:
    """
    Main Report Agent.
    Responsible for orchestrating report generation.
    """

    def __init__(self):

        self.report_builder = ReportBuilder()

        self.pdf_generator = PDFGenerator()

        self.html_generator = HTMLGenerator()

        self.json_generator = JSONGenerator()

    # =====================================================

    def generate_reports(
        self,
        analysis_result: AnalysisResult,
        output_directory: str = "generated_reports",
    ) -> ReportAgentResponse:
        """
        Generate reports in all supported formats.

        Returns:
            ReportAgentResponse
        """

        output_dir = Path(output_directory)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # -------------------------------------------------
        # Step 1 : Build Structured Report
        # -------------------------------------------------

        report = self.report_builder.build_report(
            analysis_result
        )

        # -------------------------------------------------
        # Step 2 : Generate PDF
        # -------------------------------------------------

        pdf_path = self.pdf_generator.generate(
            report=report,
            output_path=str(
                output_dir / "performance_report.pdf"
            ),
        )

        # -------------------------------------------------
        # Step 3 : Generate HTML
        # -------------------------------------------------

        html_path = self.html_generator.generate(
            report=report,
            output_path=str(
                output_dir / "performance_report.html"
            ),
        )

        # -------------------------------------------------
        # Step 4 : Generate JSON
        # -------------------------------------------------

        json_path = self.json_generator.generate(
            report=report,
            output_path=str(
                output_dir / "performance_report.json"
            ),
        )

        # -------------------------------------------------
        # Step 5 : Return Typed Response
        # -------------------------------------------------

        return ReportAgentResponse(

            report=report,

            generated_reports=GeneratedReports(

                pdf_path=pdf_path,

                html_path=html_path,

                json_path=json_path,

            ),

        )