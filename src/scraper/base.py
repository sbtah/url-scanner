import asyncio
from logging import Logger

import html2text
from lxml.html import HtmlElement, HTMLParser, fromstring, tostring
from lxml.html.clean import Cleaner
from playwright.async_api import async_playwright

from src.log import logger
from src.urls.url import Url


class BaseScraper:
    """
    Base scraper class containing logic for data extraction.
    """
    def __init__(
        self,
        headless: bool = False,
    ) -> None:
        self.headless: bool = headless
        self.logger: Logger = logger
        self._domain: str | None = None

    @staticmethod
    def viewport(*, resolution: str):
        """
        Set a viewport for next request.
        """
        resolution_params = resolution.split('x')
        return {'width': int(resolution_params[0]), 'height': int(resolution_params[1])}

    @staticmethod
    def html(*, page_source: str, base_url: str) -> HtmlElement | None:
        """
        Parse page source and return HtmlElement on success.
        - :arg page_source: Result of page.content()
        - :arg base_url: Current url
        """
        try:
            hp = HTMLParser(encoding='utf-8')
            element: HtmlElement = fromstring(
                page_source,
                parser=hp,
                base_url=base_url,
            )
            return element
        except Exception:
            return None

    @staticmethod
    def extract_text(*, html: HtmlElement) -> str | None:
        """
        Extract body from HtmlElement.
        Return entire text from all nodes on success.
        - :arg html: Lxml HtmlElement
        """
        body: list[HtmlElement] = html.xpath('/html/body')
        if len(body) == 0:
            return None
        cleaner = Cleaner(
            style=True,
            inline_style=True,
            scripts=True,
            javascript=True,
            embedded=True,
            frames=True,
            meta=True,
            annoying_tags=True,
            kill_tags=['img']
        )
        cleaned_body: HtmlElement = cleaner.clean_html(body[0])
        body_text: str = tostring(cleaned_body).decode('utf-8')
        content: str = html2text.html2text(body_text)
        return content

    @staticmethod
    def find_blocked_flags(*, content: str) -> bool:
        """
        Find certain phrases in page text that may indicate that page is flagged as a phishing.
        :param content: Entire text from the webpage.
        :return: True if any of phrases were found, implying that page is flagged.
        """
        phrases = {
            'Suspected Phishing',
            'This website has been reported for potential phishing',
            'Stop! Deceptive page ahead!',
        }
        for _ in phrases:
            if _ in content:
                return True
        return False

    def verify_page(
        self,
        *,
        url_to_check: Url,
        response,
        html: HtmlElement,
    ) -> dict | None:
        status = response.status
        page_content = self.extract_text(html=html)
        return {
            'status': status,
            'screenshot': f'{id(url_to_check)}.png',
            'blocked': self.find_blocked_flags(content=page_content),
            # 'text_content': page_content,
        }

    async def avisit_url(
        self,
        *,
        url_to_check: Url,
        user_agent: str,
        resolution: str,
        proxy_settings: dict | None = None):
        """"""
        try:
            async with async_playwright() as pw:
                # Prepare browser initial parameters
                launch_kwargs = {'headless': self.headless}
                if proxy_settings is not None:
                    launch_kwargs['proxy'] = proxy_settings

                # Launch browser.
                browser = await pw.chromium.launch(
                    args=['--start-maximized'],
                    **launch_kwargs
                )

                # Prepare and start new context.
                viewport = self.viewport(resolution=resolution)
                context = await browser.new_context(
                    viewport=viewport,
                    user_agent=user_agent,
                )
                page = await  context.new_page()

                # Navigate to a website
                response = await page.goto(
                    url_to_check.value,
                    wait_until='domcontentloaded',
                )

                # Prepare lxml HtmlElement and do whatever you want with it.
                html = self.html(page_source=await page.content(), base_url=page.url)

                # Make screenshot of requested page.
                await asyncio.sleep(5)
                await page.screenshot(path=f'{id(url_to_check)}.png', full_page=True)

                # Extract verification data from the webpage
                verify_data: dict = self.verify_page(url_to_check=url_to_check, response=response, html=html)
                url_to_check.browser_data = dict(**verify_data)

                return url_to_check
        except Exception as exc:
            self.logger.debug(
                f'({self.avisit_url.__qualname__}): exception="{exc.__class__}", '
                f'message="{exc}", url="{url_to_check.value}"', exc_info=True
            )
            return url_to_check