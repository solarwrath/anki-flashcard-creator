from logic.parsing.websites.linguee_parser import LingueeParser
from model.enums.word_category import WordCategory
from model.variants.variant import Variant
from logic.variant_augmenters.variant_augmenter import VariantAugmenter


class NounVariantAugmenter(VariantAugmenter):
    def __init__(self):
        super().__init__()
        self.linguee_parser = None

    @property
    def linguee_parser(self) -> LingueeParser:
        if self._linguee_parser is None:
            raise ValueError("LingueeParser not set")
        return self._linguee_parser

    @linguee_parser.setter
    def linguee_parser(self, value: LingueeParser) -> None:
        self._linguee_parser = value

    def can_augment(self, variant: Variant) -> bool:
        return variant.category == WordCategory.NOUN

    def _add_category_specific_data(self, variant: Variant) -> None:
        if variant.element:
            variant.gender = self.linguee_parser.get_gender(variant.element) 