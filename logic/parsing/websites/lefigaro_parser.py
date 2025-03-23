from typing import List, Optional
from bs4 import Tag, BeautifulSoup
from urllib.parse import quote

from model.enums.word_category import WordCategory
from model.enums.verb_group import VerbGroup
from model.variants.variant import Variant
from model.variants.noun_variant import NounVariant
from model.variants.verb_variant import VerbVariant
from logic.parsing.html_parser import HtmlParser
from logic.parsing.requests_parser_base import RequestsParserBase
from model.enums.conjugates_with import ConjugatesWith


class LeFigaroParser(RequestsParserBase):
    """Parser for Le Figaro conjugation page"""

    def __init__(self, query: str) -> None:
        """
        Initialize the parser with a query string.
        
        Args:
            query: The word to search for
        """
        super().__init__(query)
        self.soup = self.query_dictionary()

    def compose_query_url(self) -> str:
        """
        Compose the URL for the Le Figaro search.
        
        Returns:
            str: The complete URL for searching the word on Le Figaro
        """
        # URL encode the query to handle spaces and special characters
        encoded_query: str = quote(self.query)
        return f'https://leconjugueur.lefigaro.fr/php5/index.php?verbe={encoded_query}.html'

    def get_verb_group(self) -> VerbGroup:
        """
        Determine the verb group from the Le Figaro conjugation page.
        
        Returns:
            VerbGroup: The verb group based on the conjugation page content
            
        Raises:
            ValueError: If the verb group information cannot be found or is invalid
        """
        # Get the text from the verb group element
        group_text: Optional[str] = HtmlParser.get_text_content(self.soup, '#verbeNav > p > b')
        if not group_text:
            raise ValueError(f"Could not find verb group information for '{self.query}'")

        # Get the first word (should be "premier", "deuxième", or "troisième")
        group_word: str = group_text.split()[0].strip().lower()

        # Map to VerbGroup enum
        if group_word in ["premier", "première"]:
            return VerbGroup.FIRST
        elif group_word == "deuxième":
            return VerbGroup.SECOND
        elif group_word == "troisième":
            return VerbGroup.THIRD
            
        raise ValueError(f"Unknown verb group '{group_word}' for '{self.query}'")

    def get_conjugates_with(self) -> ConjugatesWith:
        """
        Get the auxiliary verb (être/avoir) from the Le Figaro conjugation page.
        
        Returns:
            ConjugatesWith: The auxiliary verb (ÊTRE or AVOIR)
            
        Raises:
            ValueError: If auxiliary verb information cannot be found or is invalid
        """
        # Get the text from the specified element
        aux_text: Optional[str] = HtmlParser.get_text_content(self.soup, '#verbeNav > p')
        if not aux_text:
            raise ValueError(f"Could not find auxiliary verb information for '{self.query}'")

        # Get the text and look for être/avoir
        aux_text = aux_text.strip().lower()
        
        if "être" in aux_text:
            return ConjugatesWith.ETRE
        elif "avoir" in aux_text:
            return ConjugatesWith.AVOIR
        else:
            raise ValueError(f"Could not determine auxiliary verb for '{self.query}'")

    def get_conjugates_as(self) -> List[str]:
        """
        Get the conjugation models from the Le Figaro conjugation page.
        
        Returns:
            List[str]: List of verbs that this verb conjugates like (e.g. ["parler"] for "aimer")
            
        Raises:
            ValueError: If conjugation model information cannot be found
        """
        # Get all elements with the specified selector
        model_elements: List[Tag] = self.soup.select("#sim + p > a")
        if not model_elements:
            raise ValueError(f"Could not find conjugation model information for '{self.query}'")

        # Get the text from all elements (should be model verbs)
        model_verbs = [element.get_text().strip() for element in model_elements]
        if not model_verbs or not any(model_verbs):
            raise ValueError(f"Empty conjugation models found for '{self.query}'")

        return model_verbs