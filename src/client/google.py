from src.client.base import BaseClient
from src.config import GOOGLE_API_KEY, VERSION, PROJECT_NAME
import json
from src.urls.url import Url
from typing import Collection
import asyncio
from collections import deque


class GoogleSafeBrowsingApiClient(BaseClient):
    """
    The Safe Browsing APIs (v4) let your client applications check URLs
    against Google's constantly updated lists of unsafe web resources
    """

    def __init__(self, *args, **kwargs) -> None:
        self.GOOGLE_KEY: str = GOOGLE_API_KEY
        super().__init__(*args, **kwargs)

    @property
    def headers(self) -> dict:
        """Prepare request headers for request to VirusTotalApi."""
        return {
            'Accept': 'application/json',
        }

    @property
    def google_endpoints(self) -> dict:
        """Return mapping for all used Safe Browsing Api endpoints."""
        return {
            'scan-url': f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.GOOGLE_KEY}',
        }

    async def request_scan_url(
        self,
        *,
        url_to_scan: Url,
    ) -> dict | None:
        """
        :param url_to_scan:
        :return:
        """
        data = {
            "client": {
              "clientId": "Grzegorz",
              "clientVersion": "0.0.7"
            },
            "threatInfo": {
              "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
              "platformTypes":["WINDOWS"],
              "threatEntryTypes": ["URL"],
              "threatEntries": [{'url': url_to_scan.value},],
            }
        }
        # Send a request.
        self.logger.info(
            f'SCANNING: url="{url_to_scan.value}"',
        )
        response = await self.post(url=self.google_endpoints['scan-url'], data=json.dumps(data))

        # Return json.
        return response.json() if response is not None else None

    async def run_scans(self, urls: Collection[Url]):
        """
        Sends requests to many urls.
        - :arg iterator_of_urls: Iterator of URLs.
        """
        tasks: deque = deque()
        try:
            for url in urls:
                tasks.append(
                    asyncio.create_task(
                        self.request_scan_url(
                            url_to_scan=url,
                        )
                    )
                )
            responses = await asyncio.gather(*tasks)
            return responses
        except Exception as e:
            self.logger.error(f'(get_requests) Some other exception: {e}')
            return None