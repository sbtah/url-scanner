import click
import httpx


def get_openphish_sample(file_name: str) -> None:
    """"""
    res = httpx.get('https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt')
    with open(file_name, 'w') as file:
        file.write(res.text)


def get_cert_sample(file_name: str) -> None:
    """"""
    res = httpx.get('https://hole.cert.pl/domains/v2/domains.txt')
    with open(file_name, 'w') as file:
        word: str = ''
        for char in res.text:
            if char != '\n':
                word += char
                continue
            else:
                file.write(f'http://{word}\n')
                word = ''


@click.command('open-phish-file')
def openphish() -> None:
    """"""
    file_name = 'OPEN-PHISH.txt'
    click.echo('Getting urls sample from OpenPhish...')
    get_openphish_sample(file_name=file_name)
    click.echo(f'OpenPhish sample urls saved as: {file_name}')

@click.command('cert-file')
def cert() -> None:
    """"""
    file_name = 'CERT.txt'
    click.echo(f'Getting urls sample from Cert...')
    get_cert_sample(file_name=file_name)
    click.echo(f'Cert sample urls saved as: {file_name}')
