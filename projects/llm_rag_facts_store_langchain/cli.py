import click
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from projects.llm_rag_facts_store_langchain.app_container import AppContainer
from projects.llm_rag_facts_store_langchain.services.documents_service import DocumentsService

# Load environment variables from .env file
load_dotenv()


@click.group()
def cli():
    """Simple CLI app"""

    # initialize the dependency injection container
    container = AppContainer()
    container.config.lm.embedding_model_name.from_env("OPENAI_API_EMBEDDING_MODEL", required=True)
    container.config.lm.embeddings.from_env('LLM_RAG_FACTS_STORE_LANGCHAIN_EMBEDDINGS', default='openai')
    container.config.store.chromadb_client.from_env('LLM_RAG_FACTS_STORE_LANGCHAIN_CHROMADB_CLIENT', default='in_memory')
    container.config.store.chromadb_client_http_host.from_env('LLM_RAG_FACTS_STORE_LANGCHAIN_CHROMADB_HTTP_CLIENT_HOST', default='localhost')
    container.config.store.chromadb_client_http_port.from_env('LLM_RAG_FACTS_STORE_LANGCHAIN_CHROMADB_HTTP_CLIENT_PORT', default="8000")
    container.wire(modules=[__name__])
    # pass


@cli.command()
@inject
def load(documents_service: DocumentsService = Provide[AppContainer.services.documents_service]):
    """Loads the document to the db."""
    click.echo(f"load command: loading....")

    # load documents
    documents_service.load()

    click.echo(f"load command: loaded!")


if __name__ == '__main__':
    cli()
