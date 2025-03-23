from enum import Enum


class WordCategory(Enum):
    """Categories of words in French"""
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PREPOSITION = "preposition"

    @classmethod
    def from_str(cls, text: str) -> "WordCategory | None":
        """
        Convert a string to a WordCategory enum.
        
        Args:
            text: The text to convert
            
        Returns:
            WordCategory | None: The corresponding WordCategory or None if not found
        """
        if not text:
            return None
            
        text = text.strip().lower()
        try:
            return cls(text)
        except ValueError:
            return None
