from logic.parsing.websites.playwright_parser_base import PlaywrightParserBase


class OpenIPAParser(PlaywrightParserBase):
    """Parser for OpenIPA website that provides IPA transcriptions for French words"""

    _INPUT_SELECTOR = '[class^="TextInput_input"]'
    _RESULT_SELECTOR = '[class^="ResultDisplay_display-ipa"]'

    def compose_query_url(self) -> str:
        """Return the URL to query based on self.query"""
        return "https://www.openipa.org/transcription/french"

    async def _setup_page(self) -> None:
        """Initialize page and wait for input field to be ready"""
        await super()._setup_page()
        # Wait for the input field to be ready
        await self._page.wait_for_selector(self._INPUT_SELECTOR)

    async def get_transcription(self) -> str | None:
        """Gets the IPA transcription for the word by combining all matching result elements"""
        try:
            await self._setup_page()
            
            # Type the query into the input field
            await self._page.fill(self._INPUT_SELECTOR, self.query)
            
            # Wait for the result to appear with a timeout
            await self._page.wait_for_selector(self._RESULT_SELECTOR, timeout=5000)
            
            # Get all result elements and combine their text content
            result_elements = await self._page.query_selector_all(self._RESULT_SELECTOR)
            if result_elements:
                transcription = ""
                for element in result_elements:
                    text = await element.text_content()
                    if text:
                        transcription += text
                return transcription if transcription else None
                
            return None
        except Exception as e:
            print(f"Warning: Failed to get transcription for '{self.query}': {e}")
            return None 