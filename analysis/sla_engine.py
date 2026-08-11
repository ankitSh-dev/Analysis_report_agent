"""
sla_engine.py

Deterministic SLA validation engine.

This module performs rule-based SLA validation
without using any LLM.
"""

from typing import Optional

from analysis.schemas import (
    ExecutionResult,
    MonitoringResult,
    SLAEvaluation,
    MetricStatus,
)


class SLAEngine:
    """
    Rule-based SLA validation engine.

    Evaluates only the SLA metrics for which
    corresponding agent data is available.
    """

    # ==========================
    # SLA Thresholds
    # ==========================

    RESPONSE_TIME_THRESHOLD = 800        # ms
    CPU_THRESHOLD = 90                   # %
    MEMORY_THRESHOLD = 88                # %
    DB_CONNECTION_THRESHOLD = 400        # connections
    ERROR_RATE_THRESHOLD = 1             # %

    # ==========================

    def evaluate(
        self,
        execution: Optional[ExecutionResult] = None,
        monitoring: Optional[MonitoringResult] = None,
    ) -> SLAEvaluation:
        """
        Evaluate available performance metrics
        against predefined SLA thresholds.

        The engine evaluates only the metrics whose
        corresponding input is available.
        """

        passed = []
        violated = []

        # =================================================
        # Execution Metrics
        # =================================================

        if execution is not None:

            # -----------------------------
            # Response Time
            # -----------------------------

            self._check_metric(
                metric="Response Time",
                actual=execution.avg_response_time,
                threshold=self.RESPONSE_TIME_THRESHOLD,
                passed=passed,
                violated=violated,
            )

            # -----------------------------
            # Error Rate
            # -----------------------------

            self._check_metric(
                metric="Error Rate",
                actual=execution.error_rate,
                threshold=self.ERROR_RATE_THRESHOLD,
                passed=passed,
                violated=violated,
            )

        # =================================================
        # Monitoring Metrics
        # =================================================

        if monitoring is not None:

            # -----------------------------
            # CPU
            # -----------------------------

            self._check_metric(
                metric="CPU",
                actual=monitoring.cpu_usage,
                threshold=self.CPU_THRESHOLD,
                passed=passed,
                violated=violated,
            )

            # -----------------------------
            # Memory
            # -----------------------------

            self._check_metric(
                metric="Memory",
                actual=monitoring.memory_usage,
                threshold=self.MEMORY_THRESHOLD,
                passed=passed,
                violated=violated,
            )

            # -----------------------------
            # DB Connections
            # -----------------------------

            self._check_metric(
                metric="DB Connections",
                actual=monitoring.db_connections,
                threshold=self.DB_CONNECTION_THRESHOLD,
                passed=passed,
                violated=violated,
            )

        # =================================================
        # No Performance Inputs
        # =================================================

        if not passed and not violated:

            return SLAEvaluation(
                overall_status="NOT_EVALUATED",
                severity="NOT_EVALUATED",
                violated_metrics=[],
                passed_metrics=[],
            )

        # =================================================
        # Calculate Severity
        # =================================================

        severity = self._calculate_severity(
            len(violated)
        )

        return SLAEvaluation(
            overall_status=(
                "PASS"
                if len(violated) == 0
                else "FAIL"
            ),
            severity=severity,
            violated_metrics=violated,
            passed_metrics=passed,
        )

    # ====================================================
    # Metric Evaluation
    # ====================================================

    def _check_metric(
        self,
        metric: str,
        actual: float,
        threshold: float,
        passed: list,
        violated: list,
    ):
        """
        Compare a metric against its SLA threshold.
        """

        status = (
            "PASS"
            if actual <= threshold
            else "FAIL"
        )

        metric_status = MetricStatus(
            metric=metric,
            actual=actual,
            threshold=threshold,
            status=status,
        )

        if status == "PASS":

            passed.append(
                metric_status
            )

        else:

            violated.append(
                metric_status
            )

    # ====================================================
    # Severity Calculation
    # ====================================================

    def _calculate_severity(
        self,
        violations: int,
    ) -> str:
        """
        Determine SLA severity based on
        the number of violated metrics.
        """

        if violations == 0:
            return "LOW"

        if violations <= 2:
            return "MEDIUM"

        if violations <= 4:
            return "HIGH"

        return "CRITICAL"