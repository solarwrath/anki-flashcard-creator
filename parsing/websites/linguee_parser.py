from pprint import pprint
from typing import List
from bs4 import Tag, BeautifulSoup

from model.enums.word_category import WordCategory
from model.enums.word_gender import WordGender
from model.variants.variant import Variant
from model.variants.noun_variant import NounVariant
from parsing.html_parser import HtmlParser
from parsing.websites.website_parser_base import WebsiteParserBase


class LingueeParser(WebsiteParserBase):
    def __init__(self, query: str):
        super().__init__(query)
        # TODO: Roll back to using compose_query_url and website_parser_base's fetch_html
        # when rate limiting is resolved
        with open(r"C:\Temp\livre - English translation – Linguee.htm", 'r', encoding='latin-1') as f:
            self.soup = BeautifulSoup(f.read(), 'html.parser')

    #https://www.linguee.com/english-french/search?source=auto&query=livre
    def compose_query_url(self)->str:
        return f'https://www.linguee.com/english-french/search?source=auto&query={self.query}'

    def get_gender(self, variant_element: Tag) -> WordGender | None:
        word_type = HtmlParser.get_text_content(variant_element, '.tag_wordtype')
        pprint(word_type)
        if not word_type:
            return None

        tags = word_type.split(',')
        tags = list(map(str.strip, tags))
        gender_tag = tags[-1]

        pprint(word_type)

        match gender_tag:
            case "masculine":
                return WordGender.masculine
            case "feminine":
                return WordGender.feminine

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
                return WordCategory.verb
            case "noun":
                return WordCategory.noun

        print(f"Error: Unknown category '{category}' for word '{word}'")
        return None

    def get_variant_elements(self) -> List[Tag]:
        """
        Gets all variant elements from the exact matches section
        Returns a list of BeautifulSoup Tag elements
        """
        return HtmlParser.find_elements(self.soup, '.exact .lemma')

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
            if category != WordCategory.noun:
                print(f"Warning: Skipping non-noun word '{word}' (category: {category.value})")
                continue
                
            variant = NounVariant()
            variant.category = category
            variant.word = word
            
            # Get all English definitions
            translation_elements = HtmlParser.find_elements(variant_element, '.tag_trans')
            variant.english_definitions = [
                HtmlParser.get_text_content(elem, 'a.dictLink') 
                for elem in translation_elements 
                if HtmlParser.get_text_content(elem, 'a.dictLink')
            ]
            
            variants.append(variant)
            
        return variants
