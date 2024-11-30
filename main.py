from src.client.base import BaseClient
from src.client.virus import VirusTotalApiClient
from src.client.google import GoogleSafeBrowsingApiClient
import httpx
from src.urls.url import Url
from src.scraper.scraper import Scraper
import asyncio



url = "https://www.virustotal.com/api/v3/public/urls"


def get_openphish_sample():
    res = httpx.get('https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt')
    with open('LOCAL.md', 'w') as file:
        file.write(res.text)

def load_urls():
    """"""
    with open('LOCAL.md', 'r') as file:
        lines = file.readlines()
        for line in lines:
            yield line.strip('\n')
        # return [{'url': line.strip('\n')} for line in lines]


if __name__ == '__main__':
    # print(load_urls())
    # GOOGLE
    # client = GoogleSafeBrowsingApiClient()
    # url_to_test = 'http://telnbggram.peclaro.cc/'
    #
    #
    # # urls = load_urls()
    # # for url in urls:
    # #     print(url)
    # url_object = Url(value=url_to_test)
    # response = asyncio.run(client.run_scans(urls=[url_object, ]))
    # print(response)



    # VIRUS
    client = VirusTotalApiClient()
    url_to_test = 'http://telnbggram.peclaro.cc/'
    url_object = Url(value=url_to_test)
    #
    response = client.request_scan_url(url_to_scan=url_to_test)
    # print(response)
    #
    ident = response['data']['id']
    # #
    report_response: dict = client.request_url_report(report_id=ident)
    print(report_response)
    # # client.parse_analysis_results(response=report_response)
    # print(client.get_phishing_score(response=report_response))
    #
    #
    #

