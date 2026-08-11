"""
retriever.py

Semantic retriever for the Analysis Agent.
"""

import os

from typing import List

from langchain_chroma import Chroma

from langchain_openai import AzureOpenAIEmbeddings

from analysis.schemas import RAGEvidence


CHROMA_PATH = "vector_db/chroma_db"


class RAGRetriever:
    """
    Retrieve relevant knowledge from ChromaDB.
    """

    def __init__(self):

        embeddings = AzureOpenAIEmbeddings(

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
                "AZURE_OPENAI_EMBEDDING_DEPLOYMENT"
            ),
        )

        self.vector_store = Chroma(

            persist_directory=CHROMA_PATH,

            embedding_function=embeddings,
        )

        self.retriever = (
            self.vector_store.as_retriever(

                search_kwargs={
                    "k": 5
                }
            )
        )

    # ========================================================

    def retrieve(
        self,
        query: str,
    ) -> List[RAGEvidence]:
        """
        Retrieve top relevant knowledge chunks.
        """

        documents = (
            self.retriever.invoke(query)
        )

        evidence = []

        for doc in documents:

            evidence.append(

                RAGEvidence(

                    source=doc.metadata.get(
                        "source",
                        "Unknown",
                    ),

                    section=str(
                        doc.metadata.get(
                            "page",
                            "N/A",
                        )
                    ),

                    content=doc.page_content,

                    relevance_score=0.0,
                )
            )

        return evidence