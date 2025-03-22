from dataclasses import dataclass
from typing import List

from model.enums.word_category import WordCategory


@dataclass
class Variant:
    category: WordCategory
    pronunciation: str | None
    images: list[str] | None
    english_definitions: list[str]
    word: str

    def __init__(self):
        self.pronunciation = None
        self.images = []
        self.english_definitions = []
        self.word = ""

    def to_dict(self):
        return {
            'category': self.category.value,
            'pronunciation': self.pronunciation,
            'images': self.images,
            'english_definitions': self.english_definitions,
            'word': self.word
        } 