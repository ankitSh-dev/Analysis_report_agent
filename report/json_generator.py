"""
json_generator.py

Generate JSON report from the structured LLMReportResponse.
"""

import json
from pathlib import Path

from report.schemas import LLMReportResponse


class JSONGenerator:
    """
    Generates a JSON report from the structured report.
    """

    def generate(
        self,
        report: LLMReportResponse,
        output_path: str,
    ) -> str:
        """
        Generate JSON report.

        Args:
            report: Structured report object.
            output_path: Destination JSON file path.

        Returns:
            Path to generated JSON file.
        """

        output = Path(output_path)

        with output.open("w", encoding="utf-8") as file:
            json.dump(
                report.model_dump(),
                file,
                indent=4,
                ensure_ascii=False,
            )

        return str(output)