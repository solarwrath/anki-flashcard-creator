from abc import ABC, abstractmethod
from typing import List

from model.enums.word_category import WordCategory
from model.variants.variant import Variant
from model.variants.noun_variant import NounVariant
from parsing.html_parser import HtmlParser


class VariantAugmenter(ABC):
    @abstractmethod
    def can_augment(self, variant: Variant) -> bool:
        """Check if this augmenter can handle the given variant"""
        pass

    @abstractmethod
    def augment(self, variant: Variant) -> None:
        """Add additional data to the variant based on its category"""
        pass


class NounVariantAugmenter(VariantAugmenter):
    def __init__(self, linguee_parser):
        self.linguee_parser = linguee_parser

    def can_augment(self, variant: Variant) -> bool:
        return variant.category == WordCategory.noun

    def augment(self, variant: Variant) -> None:
        if not self.can_augment(variant):
            return

        # Convert to NounVariant
        noun_variant = NounVariant()
        noun_variant.category = variant.category
        noun_variant.pronunciation = variant.pronunciation
        noun_variant.images = variant.images
        noun_variant.english_definitions = variant.english_definitions
        noun_variant.word = variant.word

        # Get gender from Linguee
        variant_elements = self.linguee_parser.get_variant_elements()
        for variant_element in variant_elements:
            variant_word = HtmlParser.get_text_content(variant_element, '.tag_lemma a.dictLink')
            if variant_word == variant.word:
                noun_variant.gender = self.linguee_parser.get_gender(variant_element)
                break

        # Update the original variant with the noun-specific data
        variant.__dict__.update(noun_variant.__dict__) 