import os

from dependency_injector import containers, providers
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter

from projects.llm_rag_facts_store_langchain.services.documents_service import DocumentsService


class ServicesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    vector_store_container = providers.DependenciesContainer()

    text_loader = providers.Singleton(
        TextLoader,
        file_path=os.path.join(os.path.dirname(__file__), "../documents", "facts.txt")
    )

    directory_loader = providers.Singleton(
        DirectoryLoader,
        path=config.documents_service.directory_loader_path,
    )

    documents_loader = providers.Selector(
        config.documents_service.documents_loader,
        local=text_loader,
        directory=directory_loader
    )

    character_text_splitter = providers.Singleton(
        CharacterTextSplitter,
        separator="\n",
        chunk_size=config.documents_service.character_text_splitter_chunk_size,
        chunk_overlap=config.documents_service.character_text_splitter_chunk_overlap
    )

    text_splitter = providers.Selector(
        config.documents_service.text_splitter,
        character_text=character_text_splitter
    )

    documents_service = providers.Singleton(
        DocumentsService,
        text_splitter=text_splitter,
        text_loader=documents_loader,
        vector_store=vector_store_container.vector_store
    )
