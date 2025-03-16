from website_parsers.website_parser_base import WebsiteParserBase


class LingueeParser(WebsiteParserBase):
    def __init__(self, query: str):
        super().__init__(query)


    def compose_query_url(self)->str:
        return f'https://www.linguee.com/english-french/search?source=auto&query={self.query}'


    def collect_data(self)->str:
        element = self.soup.select_one('.translation_desc .dictLink.featured')
        return element.text.strip()