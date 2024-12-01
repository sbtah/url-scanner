import click
from src.analyzer.base import BaseAnalyzer
import asyncio


@click.command('scan-single')
@click.argument('url')
def scan_single(url: str) -> None:
    click.echo(f'Scanning url: {url}')


@click.command('scan-file')
@click.argument('filepath')
def scan_file(filepath: str) -> None:
    """Loads and process urls from a file."""
    click.echo(f'Scanning file: {filepath}')
    analyzer = BaseAnalyzer()
    asyncio.run(analyzer.astart(file_path=filepath))


# @click.command('scan-list')
# @click.argument('urls_list')
# def scan_file(urls_list: str) -> None:
#     click.echo(f'Scanning list: {urls_list}')