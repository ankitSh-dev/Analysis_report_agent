"""
llm.py

Centralized Azure OpenAI service for the Report Agent.
"""

import os

from dotenv import load_dotenv

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from langchain_openai import AzureChatOpenAI

from report.schemas import (
    LLMReportResponse,
)


load_dotenv()


class ReportLLMService:
    """
    Azure OpenAI wrapper used only by the Report Agent.
    """

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        temperature: float = 0,
    ):

        base_llm = AzureChatOpenAI(
            azure_endpoint=os.getenv(
                "AZURE_OPENAI_ENDPOINT"
            ),
            api_key=os.getenv(
                "AZURE_OPENAI_API_KEY"
            ),
            api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION"
            ),
            azure_deployment=os.getenv(
                "AZURE_OPENAI_DEPLOYMENT"
            ),
            temperature=temperature,
        )

        self.llm = base_llm.with_structured_output(
            LLMReportResponse
        )

    # ==================================================

    def generate_report(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMReportResponse:
        """
        Generate a structured performance report
        using Azure OpenAI.
        """

        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )

        return response

    # ==================================================

    def change_model(
        self,
        model: str,
    ):
        """
        Dynamically switch the report deployment.
        """

        base_llm = AzureChatOpenAI(
            azure_endpoint=os.getenv(
                "AZURE_OPENAI_ENDPOINT"
            ),
            api_key=os.getenv(
                "AZURE_OPENAI_API_KEY"
            ),
            api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION"
            ),
            azure_deployment=model,
            temperature=0,
        )

        self.llm = base_llm.with_structured_output(
            LLMReportResponse
        )






















##------------------------------------------------ With OpenAI --------------------------------------------------------------------



# """
# llm.py

# Centralized OpenAI service for the Report Agent.
# """

# import os

# from dotenv import load_dotenv

# from langchain_core.messages import (
#     HumanMessage,
#     SystemMessage,
# )

# from langchain_openai import ChatOpenAI

# from report.schemas import (
#     LLMReportResponse,
# )

# load_dotenv()


# class ReportLLMService:
#     """
#     LLM wrapper used only by the Report Agent.
#     """

#     def __init__(
#         self,
#         model: str = "gpt-4.1-mini",
#         temperature: float = 0,
#     ):

#         base_llm = ChatOpenAI(
#             api_key=os.getenv("OPENAI_API_KEY"),
#             model=model,
#             temperature=temperature,
#         )

#         self.llm = base_llm.with_structured_output(
#             LLMReportResponse
#         )

#     # ==================================================

#     def generate_report(
#         self,
#         system_prompt: str,
#         user_prompt: str,
#     ) -> LLMReportResponse:
#         """
#         Generate a structured performance report.
#         """

#         response = self.llm.invoke(
#             [
#                 SystemMessage(content=system_prompt),
#                 HumanMessage(content=user_prompt),
#             ]
#         )

#         return response

#     # ==================================================

#     def change_model(
#         self,
#         model: str,
#     ):
#         """
#         Dynamically switch the report model.
#         """

#         base_llm = ChatOpenAI(
#             api_key=os.getenv("OPENAI_API_KEY"),
#             model=model,
#             temperature=0,
#         )

#         self.llm = base_llm.with_structured_output(
#             LLMReportResponse
#         )