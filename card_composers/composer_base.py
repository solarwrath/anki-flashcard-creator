from abc import ABC

from model.responses.response_base import Response
from website_parsers.linguee_parser import LingueeParser


class ComposerBase(ABC):
    query: str


    def __init__(self, query: str) -> None:
        self.query = query


    def compose(self)->Response:
        pass


    def get_linguee_parser(self)->LingueeParser:
        return LingueeParser(self.query)
