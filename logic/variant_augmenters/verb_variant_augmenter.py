from bs4 import Tag

from model.enums.word_category import WordCategory
from model.enums.conjugates_with import ConjugatesWith
from model.enums.verb_group import VerbGroup
from model.variants.variant import Variant
from model.variants.verb_variant import VerbVariant
from logic.variant_augmenters.variant_augmenter import VariantAugmenter
from logic.parsing.websites.lefigaro_parser import LeFigaroParser


class VerbVariantAugmenter(VariantAugmenter):
    """Augmenter for verb variants that adds conjugation information"""

    # Valid auxiliary verbs in French
    _VALID_AUXILIARIES = {"être", "avoir"}

    def can_augment(self, variant: Variant) -> bool:
        """Check if this augmenter can handle the given variant"""
        return variant.category == WordCategory.VERB

    def _add_category_specific_data(self, variant: Variant) -> None:
        """Add verb-specific data to the variant"""
        if not isinstance(variant, VerbVariant):
            return

        # Create LeFigaroParser with the variant's word
        parser = LeFigaroParser(variant.word)

        # Get verb group, auxiliary verb, and conjugation model from Le Figaro
        try:
            variant.verb_group = parser.get_verb_group()
            variant.conjugates_with = parser.get_conjugates_with()
            variant.conjugates_as = parser.get_conjugates_as()
        except ValueError as e:
            print(f"Warning: {str(e)}")

    def _create_augmented_variant(self, variant: Variant) -> VerbVariant:
        """Create a new verb variant with the same base properties"""
        augmented = VerbVariant()
        augmented.word = variant.word
        augmented.category = variant.category
        augmented.english_definitions = variant.english_definitions.copy()
        augmented.examples = variant.examples.copy()
        augmented.element = variant.element
        return augmented

