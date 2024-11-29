from src.client.base import BaseClient
from src.config import VIRUS_API_KEY


class VirusTotalApiClient(BaseClient):
    """"""

    def __init__(self, *args, **kwargs) -> None:
        self.VIRUS_KEY: str = VIRUS_API_KEY
        super().__init__(*args, **kwargs)

    @property
    def virus_endpoints(self) -> dict:
        """Return mapping for all used VirusTotal Api endpoints."""
        return {
            'scan-url': 'https://www.virustotal.com/api/v3/urls',
        }

    @property
    def headers(self) -> dict:
        """Prepare request headers for request to VirusTotalApi."""
        return {
            'Accept': 'application/json',
            'x-apikey': self.VIRUS_KEY,
        }
