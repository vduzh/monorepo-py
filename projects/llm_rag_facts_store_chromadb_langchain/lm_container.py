from dependency_injector import containers, providers
from langchain_openai import OpenAIEmbeddings


class LMContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    embeddings = providers.Singleton(
        OpenAIEmbeddings,
        model=config.embedding_model_name
    )
