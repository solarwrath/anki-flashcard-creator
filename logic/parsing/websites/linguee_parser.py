from typing import List, Optional
from bs4 import Tag, BeautifulSoup
from pathlib import Path
import chardet

from model.enums.word_category import WordCategory
from model.enums.word_gender import WordGender
from model.variants.variant import Variant
from model.variants.noun_variant import NounVariant
from model.variants.verb_variant import VerbVariant
from logic.parsing.html_parser import HtmlParser
from logic.parsing.requests_parser_base import RequestsParserBase


class LingueeParser(RequestsParserBase):
    soup: BeautifulSoup

    def __init__(self, query: str) -> None:
        """
        Initialize the parser with a query string.
        
        Args:
            query: The word to search for
            
        Raises:
            FileNotFoundError: If the cache file for the query doesn't exist
            UnicodeDecodeError: If the file encoding cannot be determined or is invalid
        """
        super().__init__(query)
        # TODO: Roll back to using compose_query_url and website_parser_base's fetch_html
        # when rate limiting is resolved
        cache_path: Path = Path("cache") / f"{query} - English translation – Linguee.htm"
        if not cache_path.exists():
            raise FileNotFoundError(f"Cache file not found for query '{query}'. Please ensure the file exists at: {cache_path}")
        
        # First try to detect the file encoding
        with open(cache_path, 'rb') as f:
            raw_data: bytes = f.read()
            result = chardet.detect(raw_data)
            encoding: str = result['encoding'] or 'latin-1'  # Fallback to latin-1 if detection fails
        
        # Try to read the file with the detected encoding
        try:
            with open(cache_path, 'r', encoding=encoding) as f:
                self.soup = BeautifulSoup(f.read(), 'html.parser')
        except UnicodeDecodeError as e:
            # If the detected encoding fails, try common encodings for French text
            for fallback_encoding in ['latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    with open(cache_path, 'r', encoding=fallback_encoding) as f:
                        self.soup = BeautifulSoup(f.read(), 'html.parser')
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise UnicodeDecodeError(
                    f"Could not decode file with any of the attempted encodings: {encoding}, latin-1, iso-8859-1, cp1252"
                ) from e

    def compose_query_url(self) -> str:
        """
        Compose the URL for the Linguee search.
        
        Returns:
            str: The complete URL for searching the word on Linguee
        """
        return f'https://www.linguee.com/english-french/search?source=auto&query={self.query}'

    def get_variant_elements(self) -> List[Tag]:
        """
        Gets all variant elements from the exact matches section.
        
        Returns:
            List[Tag]: A list of BeautifulSoup Tag elements representing each variant
        """
        return HtmlParser.find_elements(self.soup, '.exact .lemma')

    def get_examples(self, variant_element: Tag) -> List[str]:
        """
        Gets example sentences for a variant.
        
        Args:
            variant_element: The BeautifulSoup Tag containing the variant information
            
        Returns:
            List[str]: A list of example sentences in French
        """
        examples: List[str] = []

        example_lines: List[Tag] = HtmlParser.find_elements(variant_element, '.example_lines .example.line')

        for example in example_lines:
            # Get the French example text
            example_text: Optional[str] = HtmlParser.get_text_content(example, '.tag_s')
            if example_text:
                examples.append(example_text.strip())
        
        return examples

    def get_variants(self) -> List[Variant]:
        """
        Gets all variants of the word from the lemma class.
        
        Returns:
            List[Variant]: A list of Variant objects (NounVariant or VerbVariant) containing variant information
            
        Note:
            Currently supports noun and verb variants only. Other word categories are skipped.
        """
        variants: List[Variant] = []
        variant_elements: List[Tag] = self.get_variant_elements()

        for variant_element in variant_elements:
            # Get the main word
            word: Optional[str] = HtmlParser.get_text_content(variant_element, '.tag_lemma a.dictLink')
            if not word:
                continue
                
            # Check for context and append it if exists
            context: Optional[str] = HtmlParser.get_text_content(variant_element, '.tag_lemma_context')
            if context:
                word = f"{word} {context}"
                
            category: Optional[WordCategory] = self.get_word_category(variant_element) 
            if not category:
                continue

            # Create appropriate variant type based on category
            variant: Optional[Variant]
            match category:
                case WordCategory.NOUN:
                    variant = NounVariant()
                case WordCategory.VERB:
                    variant = VerbVariant()
                case _:
                    variant = Variant()

            variant.category = category
            variant.word = word
            variant.element = variant_element  # Store the HTML element

            # Get all English definitions
            translation_elements: List[Tag] = HtmlParser.find_elements(variant.element, '.tag_trans')
            variant.english_definitions = []
            
            for elem in translation_elements:
                dict_link: Optional[Tag] = elem.find('a', class_='dictLink')
                if not dict_link:
                    continue
                    
                # Get the main text content (excluding placeholder)
                main_text: str = ""
                for content in dict_link.contents:
                    if isinstance(content, str):
                        main_text += content.strip()
                    elif not content.get('class') or 'placeholder' not in content.get('class'):
                        main_text += content.get_text(strip=True)
                
                # Look for placeholder text
                placeholder: Optional[Tag] = dict_link.find(class_='placeholder')
                if placeholder:
                    placeholder_text: str = placeholder.get_text(strip=True)
                    definition: str = f"{main_text} {placeholder_text}"
                else:
                    definition: str = main_text
                    
                if definition:
                    variant.english_definitions.append(definition)

            # Get example sentences
            variant.examples = self.get_examples(variant_element)
            
            variants.append(variant)
            
        return variants

    def _process_word_type_tags(self, element: Tag) -> List[str]:
        """
        Process word type information from an element into a list of clean tags.
        
        Args:
            element: The BeautifulSoup Tag containing word type information
            
        Returns:
            List[str]: A list of cleaned and normalized tags, or empty list if no word type found
        """
        word_type: Optional[str] = HtmlParser.get_text_content(element, '.tag_wordtype')
        if not word_type:
            return []
        
        return [tag.strip().lower() for tag in word_type.split(',')]

    def get_gender(self, variant_element: Tag) -> Optional[WordGender]:
        """
        Get the gender of a word from its variant element.
        
        Args:
            variant_element: The BeautifulSoup Tag containing the variant information
            
        Returns:
            Optional[WordGender]: The gender enum value if found and valid, None otherwise
        """
        tags: List[str] = self._process_word_type_tags(variant_element)
        
        # Look for gender tag anywhere in the list
        for tag in tags:
            match tag:
                case "masculine":
                    return WordGender.MASCULINE
                case "feminine":
                    return WordGender.FEMININE
        
        return None

    def get_word_category(self, variant_element: Tag) -> WordCategory | None:
        """
        Determine the word category from the variant element.
        
        Args:
            variant_element: The HTML element containing the variant information
            
        Returns:
            WordCategory | None: The word category or None if not found
        """
        # Get the category text from the element
        category_text = HtmlParser.get_text_content(variant_element, ".tag_wordtype")
        if not category_text:
            return None

        # Convert the category text to a WordCategory enum
        return WordCategory.from_str(category_text)