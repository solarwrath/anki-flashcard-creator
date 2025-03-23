from enum import Enum


class VerbGroup(Enum):
    """French verb groups classification"""
    FIRST = "first"  # -er verbs
    SECOND = "second"  # -ir verbs
    THIRD = "third"  # -re verbs and irregular verbs

    @classmethod
    def from_str(cls, text: str) -> "VerbGroup | None":
        """
        Convert a string to a VerbGroup enum value.
        
        Args:
            text: The string to convert (e.g. "first", "1st", "1", "premier", etc.)
            
        Returns:
            VerbGroup | None: The corresponding enum value or None if invalid
        """
        if not text:
            return None
            
        # Clean up the input
        text = text.strip().lower()
        
        # Handle various formats
        if text in ["first", "1st", "1", "premier", "première"]:
            return cls.FIRST
        elif text in ["second", "2nd", "2", "deuxième"]:
            return cls.SECOND
        elif text in ["third", "3rd", "3", "troisième"]:
            return cls.THIRD
            
        return None