from typing import List
from bs4 import Tag, BeautifulSoup

from model.enums.word_category import WordCategory
from model.enums.word_gender import WordGender
from model.variants.variant import Variant
from model.variants.noun_variant import NounVariant
from logic.parsing.html_parser import HtmlParser
from logic.parsing.requests_parser_base import RequestsParserBase


class LingueeParser(RequestsParserBase):
    def __init__(self, query: str):
        super().__init__(query)
        # TODO: Roll back to using compose_query_url and website_parser_base's fetch_html
        # when rate limiting is resolved
        with open(r"C:\Temp\livre - English translation – Linguee.htm", 'r', encoding='latin-1') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')

    #https://www.linguee.com/english-french/search?source=auto&query=livre
    def compose_query_url(self)->str:
        return f'https://www.linguee.com/english-french/search?source=auto&query={self.query}'

    def get_variant_elements(self) -> List[Tag]:
        """
        Gets all variant elements from the exact matches section
        Returns a list of BeautifulSoup Tag elements
        """
        return HtmlParser.find_elements(self.soup, '.exact .lemma')

    def get_examples(self, variant_element: Tag) -> List[str]:
        """
        Gets example sentences for a variant
        Returns a list of example sentences
        """
        examples = []

        example_lines = HtmlParser.find_elements(variant_element, '.example_lines .example.line')

        for example in example_lines:
            # Get the French example text
            example_text = HtmlParser.get_text_content(example, '.tag_s')
            if example_text:
                examples.append(example_text.strip())
        
        return examples

    def get_variants(self) -> List[Variant]:
        """
        Gets all variants of the word from the lemma class
        Returns a list of Variant objects containing variant information
        """
        variants = []
        variant_elements = self.get_variant_elements()

        for variant_element in variant_elements:
            word = HtmlParser.get_text_content(variant_element, '.tag_lemma a.dictLink')
            category = self.get_word_category(variant_element, word)
            
            if not category:
                continue

            # TODO: Support other word categories (verbs, adjectives, etc.)
            if category != WordCategory.NOUN:
                print(f"Warning: Skipping non-noun word '{word}' (category: {category.value})")
                continue
                
            variant = NounVariant()
            variant.category = category
            variant.word = word
            variant.element = variant_element  # Store the HTML element

            # Get all English definitions
            translation_elements = HtmlParser.find_elements(variant.element, '.tag_trans')
            variant.english_definitions = [
                HtmlParser.get_text_content(elem, 'a.dictLink') 
                for elem in translation_elements 
                if HtmlParser.get_text_content(elem, 'a.dictLink')
            ]

            # Get example sentences
            variant.examples = self.get_examples(variant_element)
            
            variants.append(variant)
            
        return variants

    def get_gender(self, variant_element: Tag) -> WordGender | None:
        word_type = HtmlParser.get_text_content(variant_element, '.tag_wordtype')
        if not word_type:
            return None

        tags = word_type.split(',')
        tags = list(map(str.strip, tags))
        gender_tag = tags[-1]

        match gender_tag:
            case "masculine":
                return WordGender.MASCULINE
            case "feminine":
                return WordGender.FEMININE

        return None

    def get_word_category(self, variant_element: Tag, word: str) -> WordCategory | None:
        word_type = HtmlParser.get_text_content(variant_element, '.tag_wordtype')
        if not word_type:
            print(f"Error: Could not determine category for word '{word}'")
            return None

        parts = word_type.split(',')
        parts = [part.strip() for part in parts]
        category = parts[0]

        match category:
            case "verb":
                return WordCategory.VERB
            case "noun":
                return WordCategory.NOUN

        print(f"Error: Unknown category '{category}' for word '{word}'")
        return None