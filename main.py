from src.client.base import BaseClient
from src.client.virus import VirusTotalApiClient


url = "https://www.virustotal.com/api/v3/public/urls"



if __name__ == '__main__':
    url = "https://www.virustotal.com/api/v3/urls"

    payload = {"url": "https://raw.githubusercontent.com/openphish/public_feed/refs/heads/main/feed.txt"}

    client = VirusTotalApiClient()

    response = client.post(url=client.virus_endpoints['scan-url'], data=payload)

    print(response.text)

    #
    # analyzer = BaseUrlAnalyzer(url='https://github.com/sbtah/e-Scraper/blob/dev/scraper/core/settings.py')
    # print(analyzer.url_id_virus_total)
    # print(VIRUS_API_KEY)