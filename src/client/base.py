import httpx
from httpx import ConnectTimeout, Response
from src.log import logger
from logging import Logger
import time


class BaseClient:
    """
    Base Api Client used as a base for other specialized clients.
    """

    def __init__(self, *args, **kwargs) -> None:
        self._client: httpx.Client | None = None
        # self.GOOGLE_API_KEY: str = ...
        self.logger: Logger = logger

    @property
    def headers(self):
        """Should be implemented for on each child client."""
        raise NotImplementedError

    @staticmethod
    def now_timestamp() -> float:
        """Return current timestamp."""
        return time.time()

    @property
    def client(self) -> httpx.Client:
        if self._client is None:
            self._client: httpx.Client = httpx.Client
        return self._client

    # def create_url_id_virus(self, url: str) -> str:
    #     """"""
    #     return base64.urlsafe_b64encode(url.encode()).decode().strip("=")

    def get(self, *, url: str) -> Response | None:
        """
        Send a GET request to the specified url.
        Return Response object or None.
        - :arg url: Url I want to request.
        - :arg headers: Dictionary with prepared headers for this request.
        """
        try:
            with self.client() as client:
                # Start measuring response time for url.
                request_start: float = self.now_timestamp()

                # Send the request.
                res: Response = client.get(url, headers=self.headers)

                # Calculate response time for Url.
                request_end: float = self.now_timestamp()
                current_response_time: float = request_end - request_start

                self.logger.debug(
                    f'GET: status="{res.status_code}", time="{current_response_time}"',
                )
                return res
        except Exception as exc:
            self.logger.error(
                f'GET status="{exc.__class__}", message="{exc}"', exc_info=True
            )
            return None


    def post(self, url: str, data: dict | str) -> Response | None:
        """
        Send a POST request to the specified url.
        Return Response object on success.
        - :arg url: String representing an url for API endpoint.
        - :arg headers: Dictionary with prepared headers for this request.
        - :arg data: Dictionary or Json with data payload.
        """
        try:
            with self.client() as client:
                # Start measuring response time for url.
                request_start: float = self.now_timestamp()

                res: Response = client.post(
                    url=url, headers=self.headers, data=data
                )

                # Calculate response time for Url.
                request_end: float = self.now_timestamp()
                current_response_time: float = request_end - request_start

                self.logger.debug(
                    f'POST: status="{res.status_code}", time="{current_response_time}"',
                )
                return res
        except Exception as exc:
            self.logger.error(
                f'POST: status="{exc.__class__}", message="{exc}"', exc_info=True
            )
            return None