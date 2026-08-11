"""
llm.py

Centralized Azure OpenAI service for the Analysis Agent.
Returns structured Pydantic output.
"""

import os

from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from analysis.schemas import LLMAnalysisResponse


load_dotenv()


class LLMService:
    """
    Azure OpenAI wrapper for the Analysis Agent.
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

        # Structured Output Model
        self.llm = base_llm.with_structured_output(
            LLMAnalysisResponse
        )

    # ======================================================

    def invoke(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMAnalysisResponse:
        """
        Execute the Azure OpenAI model and return
        a validated LLMAnalysisResponse object.
        """

        response = self.llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )

        return response



















##---------------------------------------- With OPENAI ----------------------------------------------------------



# """
# llm.py

# Centralized OpenAI service for the Analysis Agent.
# Returns structured Pydantic output.
# """

# import os

# from dotenv import load_dotenv

# from langchain_openai import ChatOpenAI
# from langchain_core.messages import (
#     SystemMessage,
#     HumanMessage,
# )

# from analysis.schemas import LLMAnalysisResponse


# load_dotenv()


# class LLMService:
#     """
#     OpenAI wrapper for the Analysis Agent.
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

#         # Structured Output Model
#         self.llm = base_llm.with_structured_output(
#             LLMAnalysisResponse
#         )

#     # ======================================================

#     def invoke(
#         self,
#         system_prompt: str,
#         user_prompt: str,
#     ) -> LLMAnalysisResponse:
#         """
#         Execute the model and return
#         a validated LLMAnalysisResponse object.
#         """

#         response = self.llm.invoke(
#             [
#                 SystemMessage(content=system_prompt),
#                 HumanMessage(content=user_prompt),
#             ]
#         )

#         return response