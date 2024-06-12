from dependency_injector import containers, providers

from projects.llm_rag_facts_store_chromadb_langchain.containers.language_model_container import LanguageModelContainer
from projects.llm_rag_facts_store_chromadb_langchain.containers.services_container import ServicesContainer
from projects.llm_rag_facts_store_chromadb_langchain.containers.vector_store_container import VectorStoreContainer


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    lm = providers.Container(
        LanguageModelContainer,
        # config=config.lm,
        config=config,
    )

    store = providers.Container(
        VectorStoreContainer,
        lm_container=lm,
        # config=config.vector_store,
        config=config,
    )

    services = providers.Container(
        ServicesContainer,
        vector_store_container=store,
        # config=config.services,
        config=config,
    )
