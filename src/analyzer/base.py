"""

"""
import asyncio
import os
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
    """
    Analyzer class that integrates APi Clients, Scraper and a Probe class.
    """
    def __init__(self, *args, **kwargs):
        self.virus_client = VirusTotalApiClient()
        self.google_client = GoogleSafeBrowsingApiClient()
        self.prober = Probe(user_agent=USER_AGENTS[0])
        self.scraper = Scraper()
        self.logger = logger

        self.found_urls: set[Url] = set()
        self.processed_urls: set[Url] = set()
        self.queue: deque = deque()
        # Ratelimiting and other spells.
        self.max_requests: int = 4
        self.cooldown: int = 25
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
        """
        Lood urls to found urls set and proceed verification.
        :param file_path:
        :return:
        """
        if not os.path.exists(file_path):
            click.echo(f'File: {file_path} does not exist. Run a feed command maybe?')
            return

        urls_list = self.load_text_file(file_path=file_path)
        self.found_urls.update(urls_list[:100])
        await self.arun()
        self.save_to_file(file_name=file_path)

    async def arun(self):
        """
        """
        while len(self.found_urls) > 0:
            click.echo(f'Urls to Process:  {len(self.found_urls)} Urls')
            self.prepare_urls_queue()
            click.echo(f'Processing: {len(self.queue)} Urls')

            # Run requests for urls in the queue...
            await self.prober.run_probes(urls_to_check=self.queue)
            await self.google_client.run_reports(urls_to_check=self.queue)
            await self.scraper.run_visits(urls_to_check=self.queue, user_agent=USER_AGENTS[0], resolution=RESOLUTIONS[0])
            await self.virus_client.run_reports(urls_to_check=self.queue)

            self.found_urls.difference_update(self.queue)
            self.clear_queue()
            # Here I will rate limit myself because of Free tier on Virus Total...
            await asyncio.sleep(self.cooldown)
            continue
        else:
            click.echo(f'Probe liveness: {self.liveness}')
            click.echo(f'Virus detected: {self.total_virus_detected}')
            click.echo(f'Google detected: {self.total_google_detected}')
            click.echo(f'Browser detected: {self.total_webpage_blocked}')


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
        Clear urls from queue.
        Add processed urls to `processed_urls` set.
        """
        for url in self.queue:
            self.processed_urls.add(url)
        self.queue.clear()
        return

    @property
    def liveness(self) -> float:
        """"""
        total: int = len(self.processed_urls)
        if total == 0:
            return 0
        alive: int = 0
        for url in self.processed_urls:
            if url.probe_is_alive is True or url.browser_is_alive is True:
                alive += 1
        return alive / total

    @property
    def total_google_detected(self) -> float:
        """"""
        total: int = len(self.processed_urls)
        if total == 0:
            return 0
        detected: int = 0
        for url in self.processed_urls:
            if any([
                url.google_threat_types is not None,
                url.google_threats is not None,
                url.google_platform_types is not None,
            ]):
                detected += 1
        return detected / total

    @property
    def total_virus_detected(self) -> float:
        """"""
        total: int = len(self.processed_urls)
        if total == 0:
            return 0
        detected: int = 0
        for url in self.processed_urls:
            if url.is_phishing is True:
                detected += 1
        return detected / total

    @property
    def total_webpage_blocked(self) -> float:
        """"""
        total: int = len(self.processed_urls)
        if total == 0:
            return 0
        detected: int = 0
        for url in self.processed_urls:
            if url.blocked is True:
                detected += 1
        return detected / total

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