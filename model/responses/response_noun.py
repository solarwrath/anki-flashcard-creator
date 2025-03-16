from model.enums.word_category import WordCategory
from model.enums.word_gender import WordGender
from model.responses.response_base import Response


class NounResponse(Response):
    gender: WordGender

    def __init__(self, /, **data: any):
        data["category"] = WordCategory.noun
        super().__init__(**data)