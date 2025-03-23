import base64
import os
import re
from pathlib import Path
from pprint import pprint
from typing import List, NamedTuple, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from playwright.async_api import Page, ElementHandle, Response

from logic.parsing.websites.playwright_parser_base import PlaywrightParserBase


class AudioPaths(NamedTuple):
    """Container for audio paths extracted from play button"""
    mp3_path: str
    ogg_path: str
    high_quality_mp3_path: str | None
    high_quality_ogg_path: str | None


class ForvoParser(PlaywrightParserBase):
    """Parser for Forvo website that provides word pronunciations"""

    _PLAY_BUTTON_SELECTOR = ".pronunciations-list-fr .pronunciation .play"
    _PLAY_ONCLICK_PATTERN = r"Play\(\d+,\s*'(?P<mp3>[^']+)',\s*'(?P<ogg>[^']+)'(,\s*\S*?,\s*'(?P<high_mp3>[^']*)',\s*'(?P<high_ogg>[^']*).*\))?"
    _DOWNLOAD_DIR = "audio_downloads"

    def __init__(self, query: str):
        super().__init__(query)
        # Create download directory if it doesn't exist
        os.makedirs(self._DOWNLOAD_DIR, exist_ok=True)

    def compose_query_url(self) -> str:
        """Return the URL to query based on self.query"""
        # URL encode the query to handle special characters
        encoded_query = self.query.replace(" ", "+")
        return f"https://forvo.com/word/{encoded_query}/#fr"

    async def _setup_page(self) -> None:
        """Initialize page and wait for content to load"""
        await super()._setup_page()
        # Wait for pronunciations to load
        await self._page.wait_for_selector(self._PLAY_BUTTON_SELECTOR, timeout=5000)

    def _decode_path(self, encoded_path: str | None) -> str | None:
        """Decode a Base64 encoded path, return None if path is empty or invalid"""
        if not encoded_path:
            return None
        try:
            # Add padding if needed
            padding_needed = len(encoded_path) % 4
            if padding_needed:
                encoded_path += '=' * (4 - padding_needed)
            
            decoded_bytes = base64.b64decode(encoded_path)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Warning: Failed to decode path '{encoded_path}': {e}")
            return None

    def _get_local_path(self, url: str) -> str:
        """Get the local path where the audio file would be saved"""
        filename = os.path.basename(urlparse(url).path)
        return os.path.join(self._DOWNLOAD_DIR, f"{self.query}_{filename}")

    async def _check_audio_url(self, url: str) -> Tuple[bool, str | None]:
        """
        Check if audio URL is valid or already downloaded
        Returns (is_valid, local_path) where local_path is set if file exists or None if needs download
        """
        try:
            local_path = self._get_local_path(url)
            
            # Check if file already exists
            if os.path.exists(local_path):
                print(f"Audio file already exists at {local_path}")
                return True, local_path

            # If file doesn't exist, check if URL is valid
            response = await self._page.context.request.head(url)
            return response.ok, None

        except Exception as e:
            print(f"Warning: Failed to check URL '{url}': {e}")
            return False, None

    async def _download_audio(self, url: str) -> str | None:
        """Download audio file and save to disk, return local path if successful"""
        try:
            local_path = self._get_local_path(url)

            # Download the file
            response = await self._page.context.request.get(url)
            if response.ok:
                content = await response.body()
                with open(local_path, 'wb') as f:
                    f.write(content)
                print(f"Downloaded audio to {local_path}")
                return local_path
            return None
        except Exception as e:
            print(f"Warning: Failed to download audio from '{url}': {e}")
            return None

    async def get_pronunciation(self) -> List[str]:
        """Gets all pronunciation URLs from the page and downloads them"""
        try:
            await self._setup_page()
            
            # Find all play button elements
            play_buttons = await self._page.query_selector_all(self._PLAY_BUTTON_SELECTOR)

            local_paths = []
            for button in play_buttons:
                onclick = await button.get_attribute("onclick")
                if onclick:
                    match = re.match(self._PLAY_ONCLICK_PATTERN, onclick)
                    if match:
                        # Create potential URLs
                        mp3_decoded = self._decode_path(match.group('mp3'))
                        ogg_decoded = self._decode_path(match.group('ogg'))
                        high_mp3_decoded = self._decode_path(match.group('high_mp3'))
                        high_ogg_decoded = self._decode_path(match.group('high_ogg'))

                        # Build and check URLs
                        urls_to_check = []
                        if high_mp3_decoded:
                            urls_to_check.append(f"https://audio12.forvo.com/audios/mp3/{high_mp3_decoded}")
                        if mp3_decoded:
                            urls_to_check.append(f"https://audio12.forvo.com/audios/mp3/{mp3_decoded}")
                        if high_ogg_decoded:
                            urls_to_check.append(f"https://audio12.forvo.com/audios/ogg/{high_ogg_decoded}")
                        if ogg_decoded:
                            urls_to_check.append(f"https://audio12.forvo.com/audios/ogg/{ogg_decoded}")

                        # Try to download from each URL until successful
                        for url in urls_to_check:
                            is_valid, existing_path = await self._check_audio_url(url)
                            if is_valid:
                                if existing_path:
                                    local_paths.append(existing_path)
                                    break
                                if local_path := await self._download_audio(url):
                                    local_paths.append(local_path)
                                    break
            
            return local_paths
            
        except Exception as e:
            print(f"Warning: Failed to get pronunciations for '{self.query}': {e}")
            return []