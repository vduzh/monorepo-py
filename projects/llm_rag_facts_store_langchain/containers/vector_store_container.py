import os

import chromadb
from chromadb import Settings
from dependency_injector import containers, providers
from langchain_community.vectorstores import Chroma


class VectorStoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    lm_container = providers.DependenciesContainer()

    in_memory_client = providers.Singleton(chromadb.Client)

    persistent_client = providers.Singleton(
        chromadb.PersistentClient,
        path=os.path.join(os.path.expanduser('~'), "llm_rag_facts_store_langchain", "chroma_db")
    )

    http_client = providers.Singleton(
        chromadb.HttpClient,
        host=config.chromadb_client_http_host,
        port=config.chromadb_client_http_port,
        settings=Settings(allow_reset=True)
    )

    chromadb_client = providers.Selector(
        config.chromadb_client,
        in_memory=in_memory_client,
        persistent=persistent_client,
        http=http_client,
    )

    vector_store = providers.Singleton(
        Chroma,
        client=chromadb_client,
        collection_name="facts_collection",
        embedding_function=lm_container.embeddings,
    )
