import os

import chromadb
from dependency_injector import containers, providers
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

from .documents_service import DocumentsService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    embeddings = providers.Singleton(
        OpenAIEmbeddings,
        model=config.embedding_model_name
    )

    chromadb_client = providers.Singleton(chromadb.Client)

    vector_store = providers.Singleton(
        Chroma,
        client=chromadb_client,
        collection_name="facts_collection",
        embedding_function=embeddings,
    )

    text_loader = providers.Singleton(
        TextLoader,
        file_path=os.path.join(os.path.dirname(__file__), "data", "facts.txt")
    )

    text_splitter = providers.Singleton(
        CharacterTextSplitter,
        separator="\n",
        chunk_size=200,
        chunk_overlap=0
    )

    documents_service = providers.Singleton(
        DocumentsService,
        text_splitter=text_splitter,
        text_loader=text_loader,
        vector_store=vector_store
    )
