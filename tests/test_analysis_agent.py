"""
test_analysis_agent.py

Unit test for the Analysis Agent.

Tests all supported combinations of upstream agent outputs:

1. Execution only
2. Monitoring only
3. Security only
4. Execution + Monitoring
5. Execution + Security
6. Monitoring + Security
7. Execution + Monitoring + Security
"""


from analysis.analyzer import AnalysisAgent

from analysis.schemas import (
    ExecutionResult,
    MonitoringResult,
    SecurityResult,
)


# ============================================================
# Mock Builders
# ============================================================

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


# ============================================================
# Utility
# ============================================================

def print_result(title, result):

    print("\n")
    print("=" * 80)
    print(title)
    print("=" * 80)

    print(
        result.model_dump_json(
            indent=4
        )
    )


# ============================================================
# Main
# ============================================================

def main():

    execution = build_execution()

    monitoring = build_monitoring()

    security = build_security()

    agent = AnalysisAgent()

    # ========================================================
    # Scenario 1 : Execution Only
    # ========================================================

    result = agent.analyze(

        execution=execution,

        monitoring=None,

        security=None,

    )

    print_result(
        "SCENARIO 1 - EXECUTION ONLY",
        result,
    )

    # ========================================================
    # Scenario 2 : Monitoring Only
    # ========================================================

    result = agent.analyze(

        execution=None,

        monitoring=monitoring,

        security=None,

    )

    print_result(
        "SCENARIO 2 - MONITORING ONLY",
        result,
    )

    # ========================================================
    # Scenario 3 : Security Only
    # ========================================================

    result = agent.analyze(

        execution=None,

        monitoring=None,

        security=security,

    )

    print_result(
        "SCENARIO 3 - SECURITY ONLY",
        result,
    )

    # ========================================================
    # Scenario 4 : Execution + Monitoring
    # ========================================================

    result = agent.analyze(

        execution=execution,

        monitoring=monitoring,

        security=None,

    )

    print_result(
        "SCENARIO 4 - EXECUTION + MONITORING",
        result,
    )

    # ========================================================
    # Scenario 5 : Execution + Security
    # ========================================================

    result = agent.analyze(

        execution=execution,

        monitoring=None,

        security=security,

    )

    print_result(
        "SCENARIO 5 - EXECUTION + SECURITY",
        result,
    )

    # ========================================================
    # Scenario 6 : Monitoring + Security
    # ========================================================

    result = agent.analyze(

        execution=None,

        monitoring=monitoring,

        security=security,

    )

    print_result(
        "SCENARIO 6 - MONITORING + SECURITY",
        result,
    )

    # ========================================================
    # Scenario 7 : Execution + Monitoring + Security
    # ========================================================

    result = agent.analyze(

        execution=execution,

        monitoring=monitoring,

        security=security,

    )

    print_result(
        "SCENARIO 7 - EXECUTION + MONITORING + SECURITY",
        result,
    )


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
 
    main()