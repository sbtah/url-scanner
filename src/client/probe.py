import asyncio
from collections import deque
from typing import Collection

from src.client.base import BaseClient
from src.urls.url import Url


class Probe(BaseClient):
    """
    Client designed to do a probing requests to urls we want to validate.
    Return status code, server, content type for requested Url.
    """

    def __init__(self, user_agent, *args, **kwargs) -> None:
        self.user_agent: str = user_agent
        super().__init__(*args, **kwargs)

    @property
    def headers(self) -> dict:
        """Prepare headers for probing request."""
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'close',
            'User-Agent': self.user_agent,
        }

    def probe_url(
        self,
        *,
        url_to_check: Url,
    ) -> Url:
        """
        :param url_to_check:
        :return:
        """
        self.logger.debug(
            f'({self.probe_url.__qualname__}): url="{url_to_check.value}"',
        )
        response = self.get(url=url_to_check.value)
        if response is None:
            probe_data: dict = {
                'status': None,
                'probed': self.now_timestamp(),
            }
            url_to_check.probe_data = probe_data
            return url_to_check
        probe_data: dict = {
            'status': str(response.status_code),
            'bytes_downloaded': int(response.num_bytes_downloaded),
            'responded_url': str(response.url),
            'server': response.headers.get('server', None),
            'content_type': str(response.headers.get('content-type')),
            'response_time': int(response.current_response_time),
            'probed': self.now_timestamp(),
        }
        url_to_check.probe_data = dict(**probe_data)
        return url_to_check

    async def aprobe_url(
        self,
        *,
        url_to_check: Url,
    ) -> Url:
        """
        :param url_to_check:
        :return:
        """
        self.logger.debug(
            f'({self.probe_url.__qualname__}): url="{url_to_check.value}"',
        )
        response = await self.aget(url=url_to_check.value)
        if response is None:
            probe_data: dict = {
                'status': None,
                'probed': self.now_timestamp(),
            }
            url_to_check.probe_data = dict(**probe_data)
            return url_to_check
        probe_data: dict = {
            'status': str(response.status_code),
            'bytes_downloaded': int(response.num_bytes_downloaded),
            'responded_url': str(response.url),
            'server': response.headers.get('server', None),
            'content_type': str(response.headers.get('content-type')),
            'response_time': float(response.current_response_time),
            'probed': self.now_timestamp(),
        }
        url_to_check.probe_data = dict(**probe_data)
        return url_to_check

    async def run_probes(
        self,
        *,
        urls_to_check: Collection[Url],
    ) -> list[Url]:
        """
        Send asynchronous probing requests.
        - :arg urls_to_check: Urls to be requested
        - :return: List of processed Url objects.
        """
        tasks: deque = deque()
        for url in urls_to_check:
            tasks.append(
                asyncio.create_task(
                    self.aprobe_url(
                        url_to_check=url,
                    )
                )
            )
        responses = await asyncio.gather(*tasks)
        return responses