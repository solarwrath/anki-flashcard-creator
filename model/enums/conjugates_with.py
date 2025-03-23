from enum import Enum


class ConjugatesWith(Enum):
    """Enum for auxiliary verbs used in compound tenses"""
    ETRE = "être"
    AVOIR = "avoir"

    @classmethod
    def from_str(cls, value: str) -> 'ConjugatesWith | None':
        """Create enum from string, return None if invalid"""
        try:
            return next(member for member in cls if member.value == value.lower().strip())
        except StopIteration:
            return None