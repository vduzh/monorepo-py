import chromadb
from dependency_injector import containers, providers
from langchain_community.vectorstores import Chroma


class VectorStoreContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    lm_container = providers.DependenciesContainer()

    chromadb_client = providers.Singleton(chromadb.Client)

    vector_store = providers.Singleton(
        Chroma,
        client=chromadb_client,
        collection_name="facts_collection",
        embedding_function=lm_container.embeddings,
    )
