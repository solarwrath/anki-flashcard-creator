from card_composers.composer_base import ComposerBase
from model.enums.word_gender import WordGender
from model.responses.response_base import Response
from model.variants.noun_variant import NounVariant
from website_parsers.linguee_parser import LingueeParser


class ComposerNoun(ComposerBase):
    linguee_parser: LingueeParser

    def __init__(self, query: str):
        super().__init__(query)

    def compose(self, response: Response | None = None) -> Response:
        if response is None:
            response = Response()

        noun_variant = NounVariant()
        self.linguee_parser = self.get_linguee_parser()

        noun_variant.gender = self.get_gender()
        noun_variant.images = self.get_image_urls()
        
        response.variants.append(noun_variant)
        return response


    def get_gender(self)->WordGender:
        return self.linguee_parser.get_gender()