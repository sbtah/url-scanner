from src.client.base import BaseClient
from src.config import GOOGLE_API_KEY, VERSION, PROJECT_NAME
import json
from src.urls.url import Url
from typing import Collection
import asyncio
from collections import deque


class GoogleSafeBrowsingApiClient(BaseClient):
    """
    Specialized Api Client for interacting with Google Safe Browsing Api.
    https://developers.google.com/safe-browsing

    The Safe Browsing APIs (v4) let your client applications check URLs
    against Google's constantly updated lists of unsafe web resources
    """
    def __init__(self, *args, **kwargs) -> None:
        self.GOOGLE_KEY: str = GOOGLE_API_KEY
        super().__init__(*args, **kwargs)

    @property
    def headers(self) -> dict:
        """Prepare headers for requests to Google Safe Browsing Api."""
        return {
            'Accept': 'application/json',
        }

    @property
    def google_endpoints(self) -> dict:
        """Return mapping for all used Safe Browsing Api endpoints."""
        return {
            'scan-url': f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={self.GOOGLE_KEY}',
        }

    def request_url_report(
        self,
        *,
        url_to_check: Url,
    ) -> Url:
        """
        Send a post request with url we want to check in Safe Browsing Api.
        :param url_to_check: Url object that we want to validate.
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
              "threatEntries": [{'url': url_to_check.value},],
            }
        }
        # Send a request.
        self.logger.info(
            f'({self.request_url_report.__qualname__}): url="{url_to_check.value}"',
        )
        response = self.post(url=self.google_endpoints['scan-url'], data=json.dumps(data))

        # Store response data on the Url object.
        url_to_check.google_data = response.json() if response is not None else None

        # Return url object.
        return url_to_check
