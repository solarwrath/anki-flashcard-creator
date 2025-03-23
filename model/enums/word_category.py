from enum import Enum


class WordCategory(str, Enum):
    NOUN = 'noun'
    VERB = 'verb'
    ADJECTIVE = 'adjectif'
    CONJUNCTION = 'conjunction'
