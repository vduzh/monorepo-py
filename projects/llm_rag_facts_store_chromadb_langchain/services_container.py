import os

from dependency_injector import containers, providers
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter

from .documents_service import DocumentsService


class ServicesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    vector_store_container = providers.DependenciesContainer()

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
        vector_store=vector_store_container.vector_store
    )
