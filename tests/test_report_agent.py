"""
test_report_agent.py

Unit test for the Report Agent.

Tests report generation for all supported combinations
of upstream agent outputs:

1. Execution only
2. Monitoring only
3. Security only
4. Execution + Monitoring
5. Execution + Security
6. Monitoring + Security
7. Execution + Monitoring + Security
"""

from pathlib import Path

from analysis.analyzer import AnalysisAgent

from analysis.schemas import (
    ExecutionResult,
    MonitoringResult,
    SecurityResult,
)

from agents.report import ReportAgent


# ======================================================
# Mock Builders
# ======================================================

def build_execution():

    return ExecutionResult(

        job_id="JOB-10001",

        application="Internet Banking",

        scenario="UPI Payment",

        api_name="/api/v1/payment",

        total_requests=500000,

        successful_requests=498200,

        failed_requests=1800,

        avg_response_time=920.0,

        p95_response_time=1350.0,

        max_response_time=1650.0,

        throughput=280.0,

        error_rate=0.36,

        http_status=200,

    )


def build_monitoring():

    return MonitoringResult(

        cpu_usage=91,

        memory_usage=84,

        db_connections=420,

        api_latency=890,

        tps=300,

        alerts=[
            "CPU High",
            "Database Connections High",
        ],

    )


def build_security():

    return SecurityResult(

        status="FAIL",

        security_score="38%",

        issues=[
            "SQL Injection vulnerability detected",
            "Weak authentication policy",
        ],

        recommendations=[
            "Use parameterized SQL queries",
            "Enable Multi-Factor Authentication",
        ],

    )


# ======================================================
# Utility
# ======================================================

def verify_generated_files(report_response):

    print("\n")
    print("=" * 80)
    print("VERIFY GENERATED FILES")
    print("=" * 80)

    for file_path in [

        report_response.generated_reports.pdf_path,

        report_response.generated_reports.html_path,

        report_response.generated_reports.json_path,

    ]:

        exists = Path(file_path).exists()

        print(

            f"{file_path} -> "
            f"{'✅ Generated' if exists else '❌ Missing'}"

        )


# ======================================================
# Run One Scenario
# ======================================================

def run_scenario(
    title,
    analysis_agent,
    report_agent,
    execution=None,
    monitoring=None,
    security=None,
):

    print("\n")
    print("=" * 80)
    print(title)
    print("=" * 80)

    # ----------------------------------------------
    # Step 1 : Analysis Agent
    # ----------------------------------------------

    analysis_result = analysis_agent.analyze(

        execution=execution,

        monitoring=monitoring,

        security=security,

    )

    # ----------------------------------------------
    # Step 2 : Report Agent
    # ----------------------------------------------

    report_response = report_agent.generate_reports(

        analysis_result=analysis_result

    )

    # ----------------------------------------------
    # Output
    # ----------------------------------------------

    print("\nREPORT OUTPUT")

    print(

        report_response.report.model_dump_json(
            indent=4
        )

    )

    # ----------------------------------------------
    # Verify generated files
    # ----------------------------------------------

    verify_generated_files(
        report_response
    )


# ======================================================
# Main
# ======================================================

def main():

    execution = build_execution()

    monitoring = build_monitoring()

    security = build_security()

    analysis_agent = AnalysisAgent()

    report_agent = ReportAgent()

    # ==================================================
    # Scenario 1 : Execution Only
    # ==================================================

    run_scenario(

        title="SCENARIO 1 - EXECUTION ONLY",

        analysis_agent=analysis_agent,

        report_agent=report_agent,

        execution=execution,

    )

    # ==================================================
    # Scenario 2 : Monitoring Only
    # ==================================================

    run_scenario(

        title="SCENARIO 2 - MONITORING ONLY",

        analysis_agent=analysis_agent,

        report_agent=report_agent,

        monitoring=monitoring,

    )

    # ==================================================
    # Scenario 3 : Security Only
    # ==================================================

    run_scenario(

        title="SCENARIO 3 - SECURITY ONLY",

        analysis_agent=analysis_agent,

        report_agent=report_agent,

        security=security,

    )

    # ==================================================
    # Scenario 4 : Execution + Monitoring
    # ==================================================

    run_scenario(

        title="SCENARIO 4 - EXECUTION + MONITORING",

        analysis_agent=analysis_agent,

        report_agent=report_agent,

        execution=execution,

        monitoring=monitoring,

    )

    # ==================================================
    # Scenario 5 : Execution + Security
    # ==================================================

    run_scenario(

        title="SCENARIO 5 - EXECUTION + SECURITY",

        analysis_agent=analysis_agent,

        report_agent=report_agent,

        execution=execution,

        security=security,

    )

    # ==================================================
    # Scenario 6 : Monitoring + Security
    # ==================================================

    run_scenario(

        title="SCENARIO 6 - MONITORING + SECURITY",

        analysis_agent=analysis_agent,

        report_agent=report_agent,

        monitoring=monitoring,

        security=security,

    )

    # ==================================================
    # Scenario 7 : Execution + Monitoring + Security
    # ==================================================

    run_scenario(

        title="SCENARIO 7 - EXECUTION + MONITORING + SECURITY",

        analysis_agent=analysis_agent,

        report_agent=report_agent,

        execution=execution,

        monitoring=monitoring,

        security=security,

    )


# ======================================================
# Entry Point
# ======================================================

if __name__ == "__main__":

    main()