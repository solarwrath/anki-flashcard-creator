from enum import Enum


class WordCategory(str, Enum):
    noun = 'noun'
    verb = 'verb'
    adjective = 'adjective'
    conjunction = 'conjunction'
