import click

from .core import load_documents


@click.group()
def cli():
    """Simple CLI app"""
    pass


@cli.command()
def load():
    """Loads the document to the db."""
    click.echo(f"load command: loading....")
    load_documents()
    click.echo(f"load command: loaded!")


if __name__ == '__main__':
    cli()
