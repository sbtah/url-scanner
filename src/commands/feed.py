import click
import httpx


def get_openphish_sample() -> None:
    """"""
    res = httpx.get('https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt')
    with open('OPEN-PHISH.md', 'w') as file:
        file.write(res.text)


def get_cert_sample() -> None:
    """"""
    res = httpx.get('https://hole.cert.pl/domains/v2/domains.txt')
    with open('CERT.md', 'w') as file:
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
    click.echo(f'Getting urls sample from OpenPhish...')
    get_openphish_sample()


@click.command('cert-file')
def cert() -> None:
    """"""
    click.echo(f'Getting urls sample from Cert...')
    get_cert_sample()


@click.command('lol')
def lol() -> None:
    """"""
    click.echo(f'LOL')
