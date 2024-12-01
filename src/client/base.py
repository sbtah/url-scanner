import httpx
from httpx import ConnectTimeout, Response
from src.log import logger
from logging import Logger
import time


class BaseClient:
    """
    Base Api Client used as a base for other specialized clients.
    This client has interface for both async and sync request styles.
    """
    def __init__(self, *args, **kwargs) -> None:
        self._client: httpx.Client | None = None
        self._aclient: httpx.AsyncClient | None = None
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

    @property
    def aclient(self) -> httpx.AsyncClient:
        if self._aclient is None:
            self._aclient: httpx.AsyncClient = httpx.AsyncClient
        return self._aclient

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
                    f'({self.get.__qualname__}): status="{res.status_code}", request_time="{current_response_time}"',
                )

                # Attach/monkeypatch response time value to Response object.
                setattr(res, 'current_response_time', current_response_time)
                return res
        except Exception as exc:
            self.logger.error(
                f'({self.get.__qualname__}): exception="{exc.__class__}", message="{exc}"', exc_info=True
            )
            return None


    async def aget(self, *, url: str) -> Response | None:
        """
        Send a GET request to the specified url.
        Return Response object or None.
        - :arg url: Url I want to request.
        - :arg headers: Dictionary with prepared headers for this request.
        """
        try:
            async with self.aclient() as client:
                # Start measuring response time for url.
                request_start: float = self.now_timestamp()

                # Send the request.
                res: Response = await client.get(url, headers=self.headers)

                # Calculate response time for Url.
                request_end: float = self.now_timestamp()
                current_response_time: float = request_end - request_start

                self.logger.debug(
                    f'({self.aget.__qualname__}): status="{res.status_code}", request_time="{current_response_time}"',
                )

                # Attach/monkeypatch response time value to Response object.
                setattr(res, 'current_response_time', current_response_time)
                return res
        except Exception as exc:
           self.logger.debug(
                f'({self.aget.__qualname__}): exception="{exc.__class__}", message="{exc}"', exc_info=True
            )
           return None


    def post(self, url: str, data: dict | str) -> Response | None:
        """
        Send a synchronous POST request to the specified url.
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
                    f'({self.post.__qualname__}): status="{res.status_code}", request_time="{current_response_time}"',
                )

                # Attach/monkeypatch response time value to Response object.
                setattr(res, 'current_response_time', current_response_time)
                return res
        except Exception as exc:
            self.logger.error(
                f'({self.post.__qualname__}): exception="{exc.__class__}", message="{exc}"', exc_info=True
            )
            return None

    async def apost(self, url: str, data: dict | str) -> Response | None:
        """
        Send an asynchronous POST request to the specified url.
        Return Response object on success.
        - :arg url: String representing an url for API endpoint.
        - :arg headers: Dictionary with prepared headers for this request.
        - :arg data: Dictionary or Json with data payload.
        """
        try:
            async with self.client() as client:
                # Start measuring response time for url.
                request_start: float = self.now_timestamp()

                res: Response = await client.post(
                    url=url, headers=self.headers, data=data
                )

                # Calculate response time for Url.
                request_end: float = self.now_timestamp()
                current_response_time: float = request_end - request_start

                self.logger.debug(
                    f'({self.post.__qualname__}): status="{res.status_code}", request_time="{current_response_time}"',
                )
                # Attach/monkeypatch response time value to Response object.
                setattr(res, 'current_response_time', current_response_time)
                return res
        except Exception as exc:
            self.logger.error(
                f'({self.post.__qualname__}): exception="{exc.__class__}", message="{exc}"', exc_info=True
            )
            return None