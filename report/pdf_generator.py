"""
pdf_generator.py

Generate PDF report from the structured LLMReportResponse.
"""

from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from report.schemas import LLMReportResponse


class PDFGenerator:
    """
    Generates an enterprise PDF report.
    """

    def __init__(self):

        self.styles = getSampleStyleSheet()

    # ======================================================

    def generate(
        self,
        report: LLMReportResponse,
        output_path: str,
    ) -> str:
        """
        Generate the PDF report.

        Returns:
            Path of generated PDF.
        """

        output = Path(output_path)

        document = SimpleDocTemplate(str(output))

        story = []

        # --------------------------------------------------
        # Report Title
        # --------------------------------------------------

        self._add_heading(
            story,
            report.report_title,
            "Title",
        )

        story.append(Spacer(1, 20))

        # --------------------------------------------------
        # Executive Summary
        # --------------------------------------------------

        self._add_heading(
            story,
            "Executive Summary",
            "Heading2",
        )

        self._add_section(
            story,
            report.executive_summary,
        )

        # --------------------------------------------------
        # Overall Status
        # --------------------------------------------------

        self._add_heading(
            story,
            "Overall Status",
            "Heading2",
        )

        self._add_section(
            story,
            report.overall_status,
        )

        # --------------------------------------------------
        # Key Findings
        # --------------------------------------------------

        self._add_heading(
            story,
            "Key Findings",
            "Heading2",
        )

        for finding in report.key_findings:

            self._add_section(
                story,
                f"• {finding}",
            )

        # --------------------------------------------------
        # Report Sections
        # --------------------------------------------------

        for section in report.report_sections:

            self._add_heading(
                story,
                section.title,
                "Heading2",
            )

            self._add_section(
                story,
                section.content,
            )

        # --------------------------------------------------
        # Conclusion
        # --------------------------------------------------

        self._add_heading(
            story,
            "Conclusion",
            "Heading2",
        )

        self._add_section(
            story,
            report.conclusion,
        )

        document.build(story)

        return str(output)

    # ======================================================

    def _add_heading(
        self,
        story,
        text,
        style,
    ):

        story.append(
            Paragraph(
                text,
                self.styles[style],
            )
        )

    # ======================================================

    def _add_section(
        self,
        story,
        text,
    ):

        story.append(
            Paragraph(
                text,
                self.styles["BodyText"],
            )
        )

        story.append(
            Spacer(
                1,
                12,
            )
        )