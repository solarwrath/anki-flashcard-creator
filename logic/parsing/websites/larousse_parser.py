""""

class LarousseParser(RequestsParserBase):
    def __init__(self, query: str):
        super().__init__(query)

    #https://www.larousse.fr/dictionnaires/francais/livre
    def compose_query_url(self)->str:
        return f'https://www.larousse.fr/dictionnaires/francais/{self.query}'


    def get_word_category(self)->WordCategory:
        category_text = HtmlParser.get_text_content(self.soup, '#definition .header-article:first-of-type .CatgramDefinition')
        if not category_text:
            raise Exception("Could not find word category")

        categories = category_text.split(' ')
        word_category_string = categories[0].strip()
        match word_category_string:
            case "verb":
                return WordCategory.verb
            case "nom":
                return WordCategory.noun

        raise Exception(f"No such word category: {word_category_string}")
        """

