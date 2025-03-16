from model.enums.conjugates_with import ConjugatesWith
from model.enums.verb_group import VerbGroup
from model.enums.word_category import WordCategory
from model.responses.response_base import Response


class VerbResponse(Response):
    group: VerbGroup
    conjugates_with: ConjugatesWith

    def __init__(self, /, **data: any):
        data["category"] = WordCategory.verb
        super().__init__(**data)