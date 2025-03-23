from dataclasses import dataclass
from bs4 import Tag

from model.enums.word_category import WordCategory


@dataclass
class Variant:
    category: WordCategory
    pronunciation: str | None
    transcription: str | None  # IPA transcription of the word
    images: list[str] | None
    english_definitions: list[str]
    examples: list[str]  # List of example sentences
    word: str
    element: Tag | None  # Non-serializable property for the HTML element

    def __init__(self):
        self.pronunciation = None
        self.transcription = None
        self.images = []
        self.english_definitions = []
        self.examples = []
        self.word = ""
        self.element = None

    def to_dict(self):
        return {
            'category': self.category.value,
            'pronunciation': self.pronunciation,
            'transcription': self.transcription,
            'images': self.images,
            'english_definitions': self.english_definitions,
            'examples': self.examples,
            'word': self.word
        } 