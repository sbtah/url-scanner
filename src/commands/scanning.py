import click
from src.analyzer.base import BaseAnalyzer
import asyncio



@click.command('scan-single')
@click.argument('url')
def scan_single(url: str) -> None:
    """Scan a single url."""
    click.echo(f'Scanning url: {url}')
    analyzer = BaseAnalyzer()
    analyzer.single_start(url=url)


@click.command('scan-file')
@click.argument('filepath')
def scan_file(filepath: str) -> None:
    """Loads and process urls from a file."""
    click.echo(f'Scanning file: {filepath}')
    analyzer = BaseAnalyzer()
    asyncio.run(analyzer.file_start(file_path=filepath))
