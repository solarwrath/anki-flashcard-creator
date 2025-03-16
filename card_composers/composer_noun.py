from card_composers.composer_base import ComposerBase
from model.enums.word_gender import WordGender
from model.responses.response_noun import NounResponse
from website_parsers.linguee_parser import LingueeParser


class ComposerNoun(ComposerBase):
    linguee_parser: LingueeParser | None

    def __init__(self, query: str):
        super().__init__(query)

    def compose(self)->NounResponse:
        self.linguee_parser = self.get_linguee_parser()

        gender = self.get_gender()
        return NounResponse(gender = gender)


    def get_gender(self)->WordGender:
        return self.linguee_parser.get_gender()

    class Config:
        arbitrary_types_allowed: bool = True
        validate_assignment: bool = True
        defer_build: bool = True