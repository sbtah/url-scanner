from src.client.base import BaseClient
from src.client.virus import VirusTotalApiClient
from src.client.google import GoogleSafeBrowsingApiClient
from src.client.probe import Probe
import httpx
from src.urls.url import Url
from src.config import VERSION
from src.scraper.scraper import Scraper
import asyncio
from src.config import USER_AGENTS, RESOLUTIONS
from src.scraper.scraper import Scraper
import click



url = "https://www.virustotal.com/api/v3/public/urls"


def get_openphish_sample():
    res = httpx.get('https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt')
    with open('LOCAL.md', 'w') as file:
        file.write(res.text)

def load_urls():
    """"""
    with open('LOCAL.md', 'r') as file:
        lines = file.readlines()
        # for line in lines:
        #     yield line.strip('\n')
        # return [{'url': line.strip('\n')} for line in lines]
        return [Url(value=line.strip('\n')) for line in lines]


@click.command('hello')
@click.version_option(VERSION, prog_name='URL Scanner')
def hello():
    click.echo("Hello, World!")

if __name__ == '__main__':
    hello()

    # # GOOGLE
    # client = GoogleSafeBrowsingApiClient()
    # url_to_test = 'https://bantuan-customer-dana-id.0ffice.biz.id/'
    # url_to_test = 'https://wp.pl/'
    # url_object = Url(value=url_to_test)
    #
    # client.request_url_report(url_to_check=url_object)
    #
    # print(url_object.google_data)
    # print(url_object.google_threat_types)
    # print(url_object.google_platform_types)
    # print(url_object.google_threats)
    #
    #
    # # VIRUS
    # client = VirusTotalApiClient()
    # client.request_url_report(url_to_check=url_object)
    # print(url_object.virus_data)
    # print(url_object.virus_phishing_score)
    # print(url_object.virus_error)

    # urls = load_urls()
    # urls = urls[30: 36]

    # # PROBE
    # probe = Probe(user_agent=USER_AGENTS[0])
    # # probe.probe_url(url_to_check=url_object)
    # result = asyncio.run(probe.run_probes(urls_to_check=urls))
    # print([res.is_alive for res in result])

    # Playwright Verify
    # scraper = Scraper()
    # results = asyncio.run(scraper.run_visits(urls_to_check=urls, user_agent=USER_AGENTS[0], resolution=RESOLUTIONS[0]))
    # print([res.browser_data for res in results])