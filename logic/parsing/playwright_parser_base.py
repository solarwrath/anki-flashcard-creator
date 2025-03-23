import abc

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page


class PlaywrightParserBase(metaclass=abc.ABCMeta):
    """Base class for website parsers that need JavaScript support"""
    
    def __init__(self, query: str):
        self.query = query
        self._page = None
        self.soup = self._fetch_with_playwright()

    def _fetch_with_playwright(self) -> BeautifulSoup:
        """Fetch HTML using Playwright for JavaScript-enabled sites"""
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        self._page = context.new_page()
        
        url = self.compose_query_url()
        self._page.goto(url)
        # Wait for the content to load - override in subclass if needed
        self._page.wait_for_load_state('networkidle')
        
        return BeautifulSoup(self._page.content(), "html.parser")

    @abc.abstractmethod
    def compose_query_url(self) -> str:
        """Return the URL to query based on self.query"""
        pass

    def __del__(self):
        """Cleanup Playwright resources"""
        if self._page:
            context = self._page.context
            browser = context.browser
            playwright = browser.playwright
            
            self._page.close()
            context.close()
            browser.close()
            playwright.stop() 