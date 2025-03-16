from model.enums.word_category import WordCategory
from website_parsers.website_parser_base import WebsiteParserBase


class LarousseParser(WebsiteParserBase):
    def __init__(self, query: str):
        super().__init__(query)


    def compose_query_url(self)->str:
        return f'https://www.larousse.fr/dictionnaires/francais/{self.query}'


    def get_word_category(self)->WordCategory:
        category_element = self.soup.select_one('#definition .header-article:first-of-type .CatgramDefinition')
        category_element_text = category_element.text

        categories = category_element_text.split(' ')
        word_category_string = categories[0].strip()
        match word_category_string:
            case "verb":
                return WordCategory.verb
            case "nom":
                return WordCategory.noun

        raise Exception(f"No such word category: {word_category_string}")