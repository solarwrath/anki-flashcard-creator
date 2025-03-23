from abc import ABC, abstractmethod
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import TypeVar

from model.enums.word_category import WordCategory
from model.variants.variant import Variant
from logic.services.image_search_service import ImageSearchService
from logic.parsing.websites.openipa_parser import OpenIPAParser
from logic.parsing.websites.forvo_parser import ForvoParser

T = TypeVar('T', bound=Variant)


class VariantAugmenter():
    def __init__(self):
        self.image_service = ImageSearchService()
        self._executor = ThreadPoolExecutor(max_workers=1)

    @abstractmethod
    def can_augment(self, variant: Variant) -> bool:
        """Check if this augmenter can handle the given variant"""
        return True

    def augment(self, variant: Variant) -> None:
        """
        Augments the variant with additional data:
        - Category-specific data (e.g. gender for nouns)
        - Images based on word and definition
        - IPA transcription from OpenIPA
        - Pronunciations from Forvo
        """
        #self._search_images(variant)
        #self._add_transcription(variant)
        #self._add_pronunciations(variant)
        self._add_category_specific_data(variant)

    def _add_category_specific_data(self, variant: Variant) -> None:
        """Add category-specific data to the variant"""
        pass

    def _search_images(self, variant: Variant) -> None:
        """Search for images using word and first definition"""
        if variant.english_definitions:
            search_query = f"{variant.word} ({variant.english_definitions[0]})"
            variant.images = self.image_service.search_image(search_query)

    def _add_transcription(self, variant: Variant) -> None:
        """Add IPA transcription using OpenIPA"""
        try:
            # Create a new event loop in the thread
            future = self._executor.submit(
                lambda: asyncio.run(self._run_async_transcription(variant.word))
            )
            # Get the result from the future
            transcription = future.result()
            if transcription:
                variant.transcription = transcription
        except Exception as e:
            print(f"Warning: Failed to add transcription for '{variant.word}': {e}")

    def _add_pronunciations(self, variant: Variant) -> None:
        """Add pronunciations from Forvo"""
        try:
            # Create a new event loop in the thread
            future = self._executor.submit(
                lambda: asyncio.run(self._run_async_pronunciations(variant.word))
            )
            # Get the result from the future
            pronunciations = future.result()
            if pronunciations:
                variant.pronunciations = pronunciations
        except Exception as e:
            print(f"Warning: Failed to add pronunciations for '{variant.word}': {e}")

    async def _run_async_transcription(self, word: str) -> str | None:
        """Run the async transcription retrieval in a new event loop"""
        async with OpenIPAParser(word) as parser:
            return await parser.get_transcription()

    async def _run_async_pronunciations(self, word: str) -> list[str]:
        """Run the async pronunciation retrieval in a new event loop"""
        async with ForvoParser(word) as parser:
            return await parser.get_pronunciation()

    @staticmethod
    def create(category: WordCategory) -> 'VariantAugmenter':
        """Factory method to create the appropriate variant augmenter based on word category"""
        match category:
            case WordCategory.NOUN:
                from logic.variant_augmenters.noun_variant_augmenter import NounVariantAugmenter
                return NounVariantAugmenter()
            case WordCategory.VERB:
                from logic.variant_augmenters.verb_variant_augmenter import VerbVariantAugmenter
                return VerbVariantAugmenter()
            case _:
                return VariantAugmenter()

    def __del__(self):
        """Cleanup thread pool executor"""
        self._executor.shutdown(wait=False) 