from bs4 import BeautifulSoup
from playwright.async_api import Page

from logic.parsing.websites.playwright_parser_base import PlaywrightParserBase


class OpenIPAParser(PlaywrightParserBase):
    """Parser for OpenIPA website that provides IPA transcriptions for French words"""

    def compose_query_url(self) -> str:
        """Return the URL to query based on self.query"""
        return "https://www.openipa.org/transcription/french"

    async def get_transcription(self) -> str | None:
        """Gets the IPA transcription for the word"""
        try:
            await self._setup_page()

            await self._page.click('[id="checkbox-Hide Original Text"]')

            # Type the query into the input field
            input_selector = ".TextInput_input--light__wCtad"
            await self._page.fill(input_selector, self.query)
            
            # Wait for the result to appear
            result_selector = "#result .ResultDisplay_tooltip__o99_d .ResultDisplay_display-ipa--light__UeUQz"
            
            # Get the transcription
            result_elements = await self._page.query_selector_all(result_selector)

            result = ''
            for element in result_elements:
                result += await element.text_content()

            return result
        except Exception as e:
            print(f"Warning: Failed to get transcription for '{self.query}': {e}")
            return None 