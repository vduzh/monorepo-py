import os

from dotenv import load_dotenv

from projects.llm_rag_facts_store_langchain.containers.app_container import AppContainer

# Load environment variables from .env file
load_dotenv()


def init_container():
    """Initialize the dependency injection container"""

    prefix = "LLM_RAG_FACTS_STORE_LANGCHAIN"

    container = AppContainer()
    container.config.lm.embeddings.from_env(
        f'{prefix}EMBEDDINGS',
        default='openai'
    )
    container.config.lm.openai.embedding_model_name.from_env(
        "OPENAI_API_EMBEDDING_MODEL",
        required=True
    )
    container.config.store.chromadb_client.from_env(
        f'{prefix}CHROMADB_CLIENT',
        # in_memory, persistent and http supported
        default='in_memory'
    )
    container.config.store.chromadb_client_http_host.from_env(
        f'{prefix}CHROMADB_HTTP_CLIENT_HOST',
        default='localhost'
    )
    container.config.store.chromadb_client_http_port.from_env(
        f'{prefix}CHROMADB_HTTP_CLIENT_PORT',
        default=8000)
    container.config.services.documents_service.text_splitter.from_env(
        f'{prefix}DOCUMENTS_SERVICE_TEXT_SPLITTER',
        # character_text supported
        default='character_text'
    )
    container.config.services.documents_service.character_text_splitter_chunk_size.from_env(
        f'{prefix}DOCUMENTS_SERVICE_CHARACTER_TEXT_SPLITTER_CHUNK_SIZE',
        default=201
    )
    container.config.services.documents_service.character_text_splitter_chunk_overlap.from_env(
        f'{prefix}DOCUMENTS_SERVICE_CHARACTER_TEXT_SPLITTER_CHUNK_OVERLAP',
        default=0
    )
    container.config.services.documents_service.text_loader.from_env(
        f'{prefix}DOCUMENTS_SERVICE_TEXT_LOADER',
        # local and external supported
        default='local'
    )
    container.config.services.documents_service.external_text_loader_path.from_env(
        f'{prefix}DOCUMENTS_SERVICE_EXTERNAL_TEXT_LOADER_PATH',
        default=os.path.join(os.path.expanduser('~'), "llm_rag_facts_store_langchain", "documents", "facts_2.txt")
    )

    return container
