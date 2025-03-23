import abc
import random

from bs4 import BeautifulSoup
from playwright.async_api import Page, async_playwright, Playwright


class PlaywrightParserBase(metaclass=abc.ABCMeta):
    """Base class for website parsers that need JavaScript support"""
    
    _USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(self, query: str):
        self.query = query
        self._page: Page | None = None
        self._playwright: Playwright | None = None
        self.soup: BeautifulSoup | None = None

    async def __aenter__(self):
        self._playwright = await async_playwright().start()
        browser = await self._playwright.chromium.launch(
            headless=True,
        )
        
        # Configure context with settings that help bypass Cloudflare
        context = await browser.new_context(
            user_agent=random.choice(self._USER_AGENTS),
            viewport={"width": 1920, "height": 1080},
            screen={"width": 1920, "height": 1080},
            java_script_enabled=True,
            bypass_csp=True,  # Bypass Content Security Policy
            extra_http_headers={
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
            }
        )
        
        self._page = await context.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._page:
            context = self._page.context
            browser = context.browser
            
            await self._page.close()
            await context.close()
            await browser.close()
            
        if self._playwright:
            await self._playwright.stop()

    @abc.abstractmethod
    def compose_query_url(self) -> str:
        """Return the URL to query based on self.query"""
        pass

    async def _setup_page(self) -> None:
        """Initialize page and load content"""
        url = self.compose_query_url()
        await self._page.goto(url, wait_until="networkidle")
        # Create BeautifulSoup instance from the rendered page
        self.soup = BeautifulSoup(await self._page.content(), "html.parser") 