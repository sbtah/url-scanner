import click
from src.commands import feed, scanning
from src.config import PROJECT_NAME, VERSION


# Main entrypoint.
@click.group()
def cli():
    click.echo(f'Welcome to {PROJECT_NAME}')

# Commands.
cli.add_command(scanning.scan_single)
cli.add_command(scanning.scan_file)
cli.add_command(feed.openphish)
cli.add_command(feed.cert)


if __name__ == '__main__':
    cli()
