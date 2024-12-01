"""

"""
from src.client.virus import VirusTotalApiClient
from src.client.google import GoogleSafeBrowsingApiClient
from src.client.probe import Probe
from src.scraper.scraper import Scraper
from src.config import USER_AGENTS, RESOLUTIONS
from src.log import logger
from src.urls.url import Url
import time
from typing import Collection
from collections import deque
import json
import click


class BaseAnalyzer:
    """"""

    def __init__(self, *args, **kwargs):
        self.virus_client = VirusTotalApiClient()
        self.google_client = GoogleSafeBrowsingApiClient()
        self.prober = Probe(user_agent=USER_AGENTS[0])
        self.scraper = Scraper()
        self.logger = logger

        self.found_urls: set[Url] = set()
        self.processed_urls: set[Url] = set()
        self.queue: deque = deque()
        self.max_requests: int = 4
        super().__init__(*args, **kwargs)

    @staticmethod
    def now_timestamp() -> float:
        """Return current timestamp."""
        return time.time()

    @staticmethod
    def load_text_file(*, file_path: str) -> list[Url]:
        """
        Expects any text file where urls will be placed on new lines.
        Separated by newline characters : '\n'
        :param file_path:
        :return:
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()
            return [Url(value=line.strip('\n')) for line in lines]

    @staticmethod
    def create_url(*, value: str) -> Url:
        """"""
        url: Url = Url(value=value)
        return url

    def create_urls_set(self, *, urls_collection) -> set[Url]:
        """"""
        ...


    async def astart(self, *, file_path: str) -> None:
        """"""
        urls_list = self.load_text_file(file_path=file_path)
        self.found_urls.update(urls_list)
        await self.arun()
        self.save_to_file(file_name=file_path)

    async def arun(self):
        """
        """
        while len(self.found_urls) > 0:
            print(f'Urls to Process:  {len(self.found_urls)} Urls')
            self.prepare_urls_queue()
            print(f'PROCESSING  {len(self.queue)} Urls')

            # Run requests for urls in the queue...
            await self.prober.run_probes(urls_to_check=self.queue)
            # await self.scraper.run_visits(urls_to_check=self.queue, user_agent=USER_AGENTS[0], resolution=RESOLUTIONS[0])
            # await self.virus_client.

            self.found_urls.difference_update(self.queue)
            self.clear_queue()
            continue
        else:

            print([url.to_dict() for url in self.processed_urls])
            print(f'LIVENESS of feed : {self.liveness}')


    def prepare_urls_queue(self) -> None:
        """
        Add found urls to Queue up to max_requests limit.
        """
        for url in self.found_urls:
            if len(self.queue) < self.max_requests:
                self.queue.append(url)
        return

    def clear_queue(self) -> None:
        """
        Add found urls to Queue up to max_requests limit.
        """
        for url in self.queue:
            self.processed_urls.add(url)
        self.queue.clear()
        return

    @property
    def liveness(self) -> float:
        """"""
        total = len(self.processed_urls)
        alive = 0
        for url in self.processed_urls:
            if url.probe_is_alive is True or url.browser_is_alive is True:
                alive += 1
        return alive / total

    def save_to_file(self, file_name: str):
        """"""
        with open(f'Report-{file_name}.json', 'w') as file:
            file.write('[\n')
            for idx, url in enumerate(self.processed_urls):
                if idx == 0:
                    file.write(f'{json.dumps(url.to_dict())}')
                file.write(f',\n{json.dumps(url.to_dict())}')
            file.write('\n]\n')
        return