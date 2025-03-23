from dataclasses import dataclass
from bs4 import Tag

from model.enums.word_category import WordCategory


@dataclass
class Variant:
    word: str
    category: WordCategory
    images: list[str] | None
    english_definitions: list[str]
    pronunciations: list[str] | None  # List of pronunciation URLs from Forvo
    transcription: str | None  # IPA transcription of the word
    examples: list[str]  # List of example sentences

    element: Tag | None  # Non-serializable property for the HTML element

    def __init__(self):
        self.pronunciations = []
        self.transcription = None
        self.images = []
        self.english_definitions = []
        self.examples = []
        self.word = ""
        self.element = None

    def to_dict(self):
        return {
            'category': self.category.value,
            'pronunciations': self.pronunciations,
            'transcription': self.transcription,
            'images': self.images,
            'english_definitions': self.english_definitions,
            'examples': self.examples,
            'word': self.word
        } 