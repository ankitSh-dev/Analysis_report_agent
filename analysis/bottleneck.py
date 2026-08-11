"""
bottleneck.py

Rule-based Bottleneck Detection Engine.
"""

from typing import Optional

from analysis.schemas import (
    ExecutionResult,
    MonitoringResult,
    BottleneckResult,
)


class BottleneckDetector:
    """
    Detect the dominant performance bottleneck using
    whichever performance inputs are available.
    """

    CPU_THRESHOLD = 90
    MEMORY_THRESHOLD = 88
    DB_THRESHOLD = 400
    RESPONSE_TIME_THRESHOLD = 2000

    def detect(
        self,
        execution: Optional[ExecutionResult] = None,
        monitoring: Optional[MonitoringResult] = None,
    ) -> BottleneckResult:
        """
        Identify the primary bottleneck using
        available execution and monitoring data.
        """

        # =================================================
        # No Performance Data
        # =================================================

        if execution is None and monitoring is None:

            return BottleneckResult(
                bottleneck="NOT_DETERMINED",
                confidence=0.0,
                reason=(
                    "Insufficient performance data "
                    "for bottleneck detection."
                ),
                impacted_metrics=[],
            )

        # =================================================
        # Extract Available Metrics
        # =================================================

        response = (
            execution.avg_response_time
            if execution is not None
            else None
        )

        cpu = (
            monitoring.cpu_usage
            if monitoring is not None
            else None
        )

        memory = (
            monitoring.memory_usage
            if monitoring is not None
            else None
        )

        db = (
            monitoring.db_connections
            if monitoring is not None
            else None
        )

        # =================================================
        # Database Pool
        # =================================================

        if (
            db is not None
            and response is not None
            and db >= self.DB_THRESHOLD
            and response >= self.RESPONSE_TIME_THRESHOLD
        ):

            return BottleneckResult(
                bottleneck="Database Pool",
                confidence=0.95,
                reason=(
                    "High DB connections combined "
                    "with high response time."
                ),
                impacted_metrics=[
                    "DB Connections",
                    "Response Time",
                ],
            )

        # =================================================
        # High CPU
        # =================================================

        if (
            cpu is not None
            and cpu >= self.CPU_THRESHOLD
        ):

            return BottleneckResult(
                bottleneck="High CPU",
                confidence=0.92,
                reason=(
                    "CPU utilization exceeded threshold."
                ),
                impacted_metrics=[
                    "CPU",
                ],
            )

        # =================================================
        # Memory Pressure
        # =================================================

        if (
            memory is not None
            and memory >= self.MEMORY_THRESHOLD
        ):

            return BottleneckResult(
                bottleneck="Memory Pressure",
                confidence=0.90,
                reason=(
                    "Memory utilization exceeded threshold."
                ),
                impacted_metrics=[
                    "Memory",
                ],
            )

        # =================================================
        # Network Latency
        # =================================================

        if (
            response is not None
            and response >= self.RESPONSE_TIME_THRESHOLD
            and (
                cpu is None
                or cpu < self.CPU_THRESHOLD
            )
            and (
                memory is None
                or memory < self.MEMORY_THRESHOLD
            )
            and (
                db is None
                or db < self.DB_THRESHOLD
            )
        ):

            return BottleneckResult(
                bottleneck="Network Latency",
                confidence=0.85,
                reason=(
                    "High response time with available "
                    "infrastructure metrics within thresholds."
                ),
                impacted_metrics=[
                    "Response Time",
                ],
            )

        # =================================================
        # No Significant Bottleneck
        # =================================================

        return BottleneckResult(
            bottleneck="No Significant Bottleneck",
            confidence=1.0,
            reason=(
                "Available performance metrics are "
                "within acceptable thresholds."
            ),
            impacted_metrics=[],
        )