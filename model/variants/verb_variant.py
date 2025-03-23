from typing import List, Optional
from dataclasses import dataclass, field

from model.enums.word_category import WordCategory
from model.enums.conjugates_with import ConjugatesWith
from model.enums.verb_group import VerbGroup
from model.variants.variant import Variant


@dataclass
class VerbVariant(Variant):
    """A verb variant with its conjugation information"""
    conjugates_with: Optional[ConjugatesWith] = None
    conjugates_as: List[str] = field(default_factory=list)
    verb_group: Optional[VerbGroup] = None

    def __init__(self):
        super().__init__()
        self.category = WordCategory.VERB
        self.conjugates_with = None
        self.conjugates_as = []
        self.verb_group = None

    def to_dict(self) -> dict:
        """Convert the variant to a dictionary"""
        base_dict = super().to_dict()
        base_dict.update({
            'conjugates_with': self.conjugates_with.value if self.conjugates_with else None,
            'conjugates_as': self.conjugates_as,
            'verb_group': self.verb_group.value if self.verb_group else None,
        })
        return base_dict 