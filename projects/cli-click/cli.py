import click

from .core import add_numbers


@click.group()
def cli():
    """Simple CLI app"""
    pass


@cli.command()
@click.argument('name')
def greet(name):
    """Greets the user."""
    click.echo(f"Hello, {name}!")


@cli.command()
@click.argument('a', type=int)
@click.argument('b', type=int)
def add(a, b):
    """Adds two numbers."""
    result = add_numbers(a, b)
    click.echo(f"Result: {result}")


if __name__ == '__main__':
    cli()
