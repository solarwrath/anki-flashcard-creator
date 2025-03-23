from model.enums.word_category import WordCategory
from logic.variant_augmenters.variant_augmenter import VariantAugmenter


def create_variant_augmenter(category: WordCategory) -> VariantAugmenter:
    """Factory function to create the appropriate variant augmenter based on word category"""
    return VariantAugmenter.create(category)


__all__ = ['VariantAugmenter', 'create_variant_augmenter']
