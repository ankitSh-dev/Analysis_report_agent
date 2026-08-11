"""
html_generator.py

Generate HTML report from the structured LLMReportResponse.
"""

from pathlib import Path

from report.schemas import LLMReportResponse


class HTMLGenerator:
    """
    Generates an enterprise HTML performance report.
    """

    def generate(
        self,
        report: LLMReportResponse,
        output_path: str,
    ) -> str:
        """
        Generate HTML report.

        Returns:
            Path to generated HTML file.
        """

        html = self._build_html(report)

        output = Path(output_path)

        output.write_text(
            html,
            encoding="utf-8",
        )

        return str(output)

    # =====================================================

    def _build_html(
        self,
        report: LLMReportResponse,
    ) -> str:

        findings = "".join(
            f"<li>{finding}</li>"
            for finding in report.key_findings
        )

        sections = ""

        for section in report.report_sections:

            sections += f"""
            <section class="card">
                <h2>{section.title}</h2>
                <p>{section.content}</p>
            </section>
            """

        return f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>{report.report_title}</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background:#f4f6f9;
    margin:40px;
}}

.container {{
    max-width:1100px;
    margin:auto;
}}

.card {{
    background:white;
    padding:20px;
    margin-bottom:20px;
    border-radius:8px;
    box-shadow:0 2px 8px rgba(0,0,0,.1);
}}

.status {{
    font-weight:bold;
    color:#0b5394;
}}

h1 {{
    text-align:center;
}}

</style>

</head>

<body>

<div class="container">

<h1>{report.report_title}</h1>

<div class="card">

<h2>Executive Summary</h2>

<p>{report.executive_summary}</p>

</div>

<div class="card">

<h2>Overall Status</h2>

<p class="status">{report.overall_status}</p>

</div>

<div class="card">

<h2>Key Findings</h2>

<ul>

{findings}

</ul>

</div>

{sections}

<div class="card">

<h2>Conclusion</h2>

<p>{report.conclusion}</p>

</div>

</div>

</body>

</html>
"""