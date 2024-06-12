from dependency_injector import containers, providers
from langchain_openai import OpenAIEmbeddings


class LanguageModelContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    openai_embeddings = providers.Singleton(
        OpenAIEmbeddings,
        model=config.embedding_model_name
    )

    embeddings = providers.Selector(
        config.embeddings,
        openai=openai_embeddings,
    )
