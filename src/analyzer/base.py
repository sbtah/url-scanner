"""

"""
from src.client.virus import VirusTotalApiClient
from src.log import logger
from src.urls.url import Url


class BaseAnalyzer:
    """"""

    def __init__(self) -> None:
        self.virus_api_client: VirusTotalApiClient = VirusTotalApiClient()
        self.virus_url_reported_minimum: int = 3
        self.google_api_client = ...
        self.probe = ...
        self.browser = ...
        self.logger = logger


    def feed_from_file(self, *, file_path: str):
        """
        MD format: Just urls on new lines.
        JSON format:
        CSV
        :param file_path:
        :return:
        """
        ...

    @staticmethod
    def create_url_object(self, *, value: str):
        """"""
        url: Url = Url(value=value)
        return url
