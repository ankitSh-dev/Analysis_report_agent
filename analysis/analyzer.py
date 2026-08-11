"""
analyzer.py

Main Analysis Agent Orchestrator.
"""

from typing import Optional

from analysis.schemas import (
    ExecutionResult,
    MonitoringResult,
    SecurityResult,
    AnalysisResult,
    Recommendation,
    SLAEvaluation,
    BottleneckResult,
)

from analysis.sla_engine import SLAEngine
from analysis.bottleneck import BottleneckDetector
from analysis.historical import HistoricalComparator

from vector_db.retriever import RAGRetriever

from analysis.prompts import (
    SYSTEM_PROMPT,
    ANALYSIS_PROMPT,
)

from analysis.llm import LLMService


class AnalysisAgent:
    """
    Enterprise Analysis Agent.

    Responsible for orchestrating the complete
    performance analysis workflow using whatever
    upstream agent outputs are available.
    """

    def __init__(self):

        self.sla_engine = SLAEngine()
        self.bottleneck_detector = BottleneckDetector()
        self.historical = HistoricalComparator()
        self.rag = RAGRetriever()
        self.llm = LLMService()

    # =====================================================
    # Main Analysis
    # =====================================================

    def analyze(
        self,
        execution: Optional[ExecutionResult] = None,
        monitoring: Optional[MonitoringResult] = None,
        security: Optional[SecurityResult] = None,
    ) -> AnalysisResult:
        """
        Complete Performance Analysis Pipeline.

        The Analysis Agent dynamically processes
        whichever upstream agent results are available.
        """

        # =================================================
        # Step 1 : SLA Evaluation
        # =================================================

        if execution is not None and monitoring is not None:

            sla_result = self.sla_engine.evaluate(
                execution,
                monitoring,
            )

        else:

            sla_result = SLAEvaluation(
                overall_status="NOT_EVALUATED",
                severity="NOT_EVALUATED",
                violated_metrics=[],
                passed_metrics=[],
            )

        # =================================================
        # Step 2 : Bottleneck Detection
        # =================================================

        if execution is not None and monitoring is not None:

            bottleneck = self.bottleneck_detector.detect(
                execution,
                monitoring,
            )

        else:

            bottleneck = BottleneckResult(
                bottleneck="NOT_DETERMINED",
                confidence=0.0,
                reason=(
                    "Insufficient execution and monitoring "
                    "data for bottleneck detection."
                ),
                impacted_metrics=[],
            )

        # =================================================
        # Step 3 : Historical Comparison
        # =================================================

        if execution is not None:

            historical = self.historical.find_similar(
                execution
            )

        else:

            historical = self._empty_historical_result()

        # =================================================
        # Step 4 : RAG Retrieval
        # =================================================

        if execution is not None:

            rag_results = self.rag.retrieve(
                self._build_query(
                    execution,
                    bottleneck,
                )
            )

        else:

            rag_results = []

        # =================================================
        # Step 5 : Build LLM Prompt
        # =================================================

        prompt = self._build_prompt(
            execution=execution,
            monitoring=monitoring,
            security=security,
            sla=sla_result,
            bottleneck=bottleneck,
            historical=historical,
            rag=rag_results,
        )

        # =================================================
        # Step 6 : LLM Analysis
        # =================================================

        llm_response = self.llm.invoke(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
        )

        # =================================================
        # Step 7 : Build Final AnalysisResult
        # =================================================

        return self._build_analysis_result(
            llm_response=llm_response,
            sla=sla_result,
            bottleneck=bottleneck,
            historical=historical,
            rag=rag_results,
        )

    # =====================================================
    # RAG Query
    # =====================================================

    def _build_query(
        self,
        execution: ExecutionResult,
        bottleneck: BottleneckResult,
    ) -> str:

        return (
            f"""
            Scenario : {execution.scenario}

            API : {execution.api_name}

            Response Time : {execution.avg_response_time}

            Bottleneck : {bottleneck.bottleneck}
            """
        )

    # =====================================================
    # Prompt Builder
    # =====================================================

    def _build_prompt(
        self,
        execution: Optional[ExecutionResult],
        monitoring: Optional[MonitoringResult],
        security: Optional[SecurityResult],
        sla: SLAEvaluation,
        bottleneck: BottleneckResult,
        historical,
        rag,
    ) -> str:
        """
        Build the LLM prompt using only the
        information that is currently available.
        """

        # -------------------------------------------------
        # Execution
        # -------------------------------------------------

        if execution is not None:

            execution_text = execution.model_dump_json(
                indent=2
            )

        else:

            execution_text = (
                "Execution Agent output is not available "
                "for this request."
            )

        # -------------------------------------------------
        # Monitoring
        # -------------------------------------------------

        if monitoring is not None:

            monitoring_text = monitoring.model_dump_json(
                indent=2
            )

        else:

            monitoring_text = (
                "Monitoring Agent output is not available "
                "for this request."
            )

        # -------------------------------------------------
        # Security
        # -------------------------------------------------

        if security is not None:

            security_text = security.model_dump_json(
                indent=2
            )

        else:

            security_text = (
                "Security Agent output is not available "
                "for this request."
            )

        # -------------------------------------------------
        # RAG Evidence
        # -------------------------------------------------

        if rag:

            rag_text = "\n\n".join(
                evidence.content
                for evidence in rag
            )

        else:

            rag_text = (
                "No RAG evidence is available "
                "for this request."
            )

        # -------------------------------------------------
        # Final Prompt
        # -------------------------------------------------

        return ANALYSIS_PROMPT.format(

            execution=execution_text,

            monitoring=monitoring_text,

            security=security_text,

            sla=sla.model_dump_json(
                indent=2
            ),

            bottleneck=bottleneck.model_dump_json(
                indent=2
            ),

            historical=historical.model_dump_json(
                indent=2
            ),

            rag=rag_text,

        )

    # =====================================================
    # Empty Historical Result
    # =====================================================

    def _empty_historical_result(self):

        from analysis.schemas import HistoricalSearchResult

        return HistoricalSearchResult(
            total_matches=0,
            matches=[],
        )

    # =====================================================
    # Final Analysis Result
    # =====================================================

    def _build_analysis_result(
        self,
        llm_response,
        sla,
        bottleneck,
        historical,
        rag,
    ) -> AnalysisResult:
        """
        Convert the structured LLM response and
        deterministic results into the final
        AnalysisResult.
        """

        recommendations = []

        for item in llm_response.recommendations:

            recommendations.append(

                Recommendation(
                    priority=item.priority,
                    title=item.title,
                    description=item.description,
                )

            )

        return AnalysisResult(

            overall_status=llm_response.overall_status,

            sla_status=sla.overall_status,

            bottleneck=bottleneck.bottleneck,

            root_cause=llm_response.root_cause,

            confidence_score=llm_response.confidence_score,

            recommendations=recommendations,

            historical_matches=historical.matches,

            rag_evidence=rag,

            summary=llm_response.executive_summary,

        )