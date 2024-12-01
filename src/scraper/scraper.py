from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
from src.scraper.base import BaseScraper
import asyncio
from collections import deque
from typing import Iterable, Collection
from asyncio import Future
from src.urls.url import Url


class Scraper(BaseScraper):

    def __init__(self, max_retries: int = 4, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def run_visits(
        self,
        *,
        urls_to_check: Collection[Url],
        user_agent: str,
        resolution: str,
        proxy_settings: dict | None = None
    ) -> list[Url]:
        """
        Send requests to the collection of urls.
        - :arg urls: Url objects to iterate over.
        """
        assert len(urls_to_check) > 0, 'There are no Url to request!'
        tasks: deque = deque()

        for url in urls_to_check:
            tasks.append(
                asyncio.create_task(
                    self.avisit_url(
                        url_to_check=url,
                        user_agent=user_agent,
                        resolution=resolution,
                        proxy_settings=proxy_settings,
                    )
                )
            )
        responses = await asyncio.gather(*tasks)
        return responses