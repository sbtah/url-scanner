import base64

from src.client.base import BaseClient
from src.config import VIRUS_API_KEY
from src.urls.url import Url


class VirusTotalApiClient(BaseClient):
    """
    Specialized Api Client for interacting with VirusTotal API v3.
    https://docs.virustotal.com/reference/url

    Right now client's interface allows for requests to standard VirusTotal (open) endpoints.
    There are also `private` endpoints.

    TL;DR: See files or URLs through the eyes of VirusTotal without uploading them to the main threat corpus,
    in other words, without sharing with other VirusTotal users or distributing them beyond your organization.
    Static, dynamic, network and similarity analysis included for files,
    as well as automated threat intel enrichment,
    but it will NOT contain our multi-antivirus or url-scan partners verdicts.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.VIRUS_KEY: str = VIRUS_API_KEY
        super().__init__(*args, **kwargs)

    @property
    def headers(self) -> dict:
        """Prepare headers for request to VirusTotalApi."""
        return {
            'Accept': 'application/json',
            'x-apikey': self.VIRUS_KEY,
        }

    @property
    def virus_endpoints(self) -> dict:
        """Return mapping for all used VirusTotal Api endpoints."""
        return {
            'scan-url': 'https://www.virustotal.com/api/v3/urls',
            # 'url-analysis': 'https://www.virustotal.com/api/v3/analyses/{report_id}'
            # `url_id` must be calculated before.
            'url-report': 'https://www.virustotal.com/api/v3/urls/{url_id}',
            'private-url-report': ...,
        }

    @staticmethod
    def create_url_id(*, url: str) -> str:
        """
        Create Url identifier according to:
        https://docs.virustotal.com/reference/url#url-identifiers
        This identifier is needed in request to `url-report` endpoint.
        :param url: String representing url we are analyzing.
        :return: String representing an Url identifier.
        """
        return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    def request_url_report(
        self,
        *,
        url_to_check: Url,
    ) -> Url:
        """
        Send a get request to analysis report endpoint:
        https://www.virustotal.com/api/v3/urls/{id}

        TODO:
        Implement a private endpoint.
        https://www.virustotal.com/api/v3/private/urls/{id}

        :param url_to_check: Url object that we want to validate.
        :return: Updated Url object.
        """
        # Prepare Url identifier for current Url object.
        url_identifier: str = self.create_url_id(url=url_to_check.value)
        # Send a request.
        self.logger.info(
            f'({self.request_url_report.__qualname__}): url="{url_to_check.value}"',
        )
        response = self.get(url=self.virus_endpoints['url-report'].format(url_id=url_identifier))

        # Store response data on the Url object.
        url_to_check.virus_data = dict(**response.json()) if response is not None else None

        # Return url object.
        return url_to_check


    def request_scan_url(
        self,
        *,
        url_to_scan: Url,
    ) -> dict | None:
        """
        Send POST request to `scan-url` VirusTotal Api Endpoint.
        :param url_to_scan: Url object which we want to be scanned by VirusTotal.
        :return: Dictionary with needed data.
        """
        # Prepare a payload to send.
        payload = {"url": url_to_scan.value}

        # Send a request.
        self.logger.info(
            f'({self.request_scan_url.__qualname__}):: url="{url_to_scan.value}"',
        )
        response = self.post(url=self.virus_endpoints['scan-url'], data=payload)

        # Return json.
        return response.json() if response is not None else None
