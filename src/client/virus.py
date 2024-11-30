from src.client.base import BaseClient
from src.config import VIRUS_API_KEY
import base64


class VirusTotalApiClient(BaseClient):
    """
    Specialized Api Client for interacting with VirusTotal API v3.
    https://docs.virustotal.com/reference/url
    """

    def __init__(self, *args, **kwargs) -> None:
        self.VIRUS_KEY: str = VIRUS_API_KEY
        super().__init__(*args, **kwargs)

    @property
    def virus_endpoints(self) -> dict:
        """Return mapping for all used VirusTotal Api endpoints."""
        return {
            'scan-url': 'https://www.virustotal.com/api/v3/urls',
            'url-report': 'https://www.virustotal.com/api/v3/analyses/{report_id}'
            # 'url-report': 'https://www.virustotal.com/api/v3/urls/{url_id}'
        }

    @property
    def headers(self) -> dict:
        """Prepare request headers for request to VirusTotalApi."""
        return {
            'Accept': 'application/json',
            'x-apikey': self.VIRUS_KEY,
        }

    @staticmethod
    def create_url_id(*, url: str) -> str:
        """
        Create Url identifier according to:
        https://docs.virustotal.com/reference/url#url-identifiers
        :param url: String representing url we are analyzing.
        :return: String representing an Url identifier.
        """
        return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    def request_scan_url(
        self,
        *,
        url_to_scan: str,
    ) -> dict | None:
        """
        Send POST request to `scan-url` VirusTotal Api Endpoint.
        :param url_to_scan: String representing the url we want to scan.
        :return: Dictionary with needed data.
        """
        # Prepare a payload to send.
        payload = {"url": url_to_scan}

        # Send a request.
        self.logger.info(
            f'SCANNING: url="{url_to_scan}"',
        )
        response = self.post(url=self.virus_endpoints['scan-url'], data=payload)

        # Return json.
        return response.json() if response is not None else None


    def request_url_report(
        self,
        *,
        report_id: str,
    ) -> dict | None:
        """"""
        # url_identifier: str = self.create_url_id(url=url)
        response = self.get(url=self.virus_endpoints['url-report'].format(report_id=report_id))
        return response.json() if response is not None else None

    @staticmethod
    def get_phishing_score(*, response: dict) -> int:
        """
        :param response:
        :return:
        """
        analysis_results: dict = response['data']['attributes']['last_analysis_stats']
        return int(analysis_results['malicious'])

    @staticmethod
    def get_harmless_score(*, response: dict) -> int:
        """
        :param response:
        :return:
        """
        analysis_results: dict = response['data']['attributes']['last_analysis_stats']
        return int(analysis_results['harmless'])

    @staticmethod
    def get_undetected_score(*, response: dict) -> int:
        """
        :param response:
        :return:
        """
        analysis_results: dict = response['data']['attributes']['last_analysis_stats']
        return int(analysis_results['undetected'])

    @staticmethod
    def get_suspicious_score(*, response: dict) -> int:
        """
        :param response:
        :return:
        """
        analysis_results: dict = response['data']['attributes']['last_analysis_stats']
        return int(analysis_results['suspicious'])

    @staticmethod
    def get_malicious_score(*, response: dict) -> int:
        """
        :param response:
        :return:
        """
        analysis_results: dict = response['data']['attributes']['last_analysis_stats']
        return int(analysis_results['malicious'])

