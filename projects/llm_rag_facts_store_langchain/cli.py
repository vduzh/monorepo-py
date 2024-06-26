import click
from dependency_injector.wiring import Provide, inject
from dotenv import load_dotenv

from projects.llm_rag_facts_store_langchain.containers.app_container import AppContainer
from projects.llm_rag_facts_store_langchain.core import init_container
from projects.llm_rag_facts_store_langchain.services.documents_service import DocumentsService

# Load environment variables from .env file
load_dotenv()


@click.group()
def cli():
    """Simple CLI app"""

    container = init_container()
    container.wire(modules=[__name__])


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
