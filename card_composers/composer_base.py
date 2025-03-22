from abc import ABC

from model.responses.response_base import Response
from website_parsers.larousse_parser import LarousseParser
from website_parsers.linguee_parser import LingueeParser
from services.image_search_service import ImageSearchService


class ComposerBase(ABC):
    query: str
    image_search_service: ImageSearchService


    def __init__(self, query: str) -> None:
        self.query = query
        self.image_search_service = ImageSearchService()


    def compose(self, response: Response | None = None) -> Response:
        if response is None:
            response = Response()

        response.images = self.get_image_urls()

        return response


    def get_linguee_parser(self)->LingueeParser:
        return LingueeParser(self.query)


    def get_larousse_parser(self)->LarousseParser:
        return LarousseParser(self.query)


    def get_image_urls(self)->list[str]:
        """Gets the image URLs for the word using Google Custom Search API"""
        return self.image_search_service.search_image(self.query)
