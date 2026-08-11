"""
ingest.py

Builds the Chroma Vector Database.

Run this file once whenever
new documents are added.
"""

import os

from dotenv import load_dotenv

from langchain_community.document_loaders import (
    PyPDFLoader,
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)

from langchain_openai import AzureOpenAIEmbeddings

from langchain_chroma import Chroma


load_dotenv()


# ============================================================
# Configuration
# ============================================================

DOCUMENTS = [

    "knowledge_base/historical_execution_report.pdf",

    "knowledge_base/incident_knowledge_base.pdf",

    "knowledge_base/performance_sla_runbook.pdf",

]

CHROMA_PATH = "vector_db/chroma_db"


# ============================================================
# Load PDFs
# ============================================================

def load_documents():

    documents = []

    for pdf in DOCUMENTS:

        loader = PyPDFLoader(pdf)

        documents.extend(
            loader.load()
        )

    return documents


# ============================================================
# Split Documents
# ============================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    return splitter.split_documents(
        documents
    )


# ============================================================
# Build Vector DB
# ============================================================

def build_vector_db():

    documents = load_documents()

    chunks = split_documents(
        documents
    )

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

    Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory=CHROMA_PATH,
    )

    print(
        "Vector Database Created Successfully."
    )


# ============================================================

if __name__ == "__main__":

    build_vector_db()