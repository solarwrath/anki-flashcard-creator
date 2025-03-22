from dataclasses import dataclass
from typing import List

from model.enums.word_category import WordCategory
from model.enums.word_gender import WordGender
from model.variants.variant import Variant


@dataclass
class NounVariant(Variant):
    gender: WordGender | None

    def __init__(self):
        super().__init__()
        self.gender = None

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict['gender'] = self.gender.value if self.gender else None
        return base_dict 