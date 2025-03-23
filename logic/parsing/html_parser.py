from typing import List, Optional
from bs4 import BeautifulSoup, Tag


class HtmlParser:
    @staticmethod
    def get_text(element: Optional[Tag]) -> Optional[str]:
        """Safely get text from a BeautifulSoup element"""
        if element is None:
            return None
        return element.get_text(strip=True)

    @staticmethod
    def get_attribute(element: Optional[Tag], attribute: str) -> Optional[str]:
        """Safely get an attribute from a BeautifulSoup element"""
        if element is None:
            return None
        return element.get(attribute)

    @staticmethod
    def find_element(soup: BeautifulSoup, selector: str) -> Optional[Tag]:
        """Find a single element using CSS selector"""
        return soup.select_one(selector)

    @staticmethod
    def find_elements(soup: BeautifulSoup, selector: str) -> List[Tag]:
        """Find multiple elements using CSS selector"""
        return soup.select(selector)

    @staticmethod
    def find_element_by_class(soup: BeautifulSoup, class_name: str) -> Optional[Tag]:
        """Find a single element by class name"""
        return soup.find(class_=class_name)

    @staticmethod
    def find_elements_by_class(soup: BeautifulSoup, class_name: str) -> List[Tag]:
        """Find multiple elements by class name"""
        return soup.find_all(class_=class_name)

    @staticmethod
    def find_element_by_id(soup: BeautifulSoup, id_name: str) -> Optional[Tag]:
        """Find a single element by ID"""
        return soup.find(id=id_name)

    @staticmethod
    def find_element_by_tag_and_class(soup: BeautifulSoup, tag: str, class_name: str) -> Optional[Tag]:
        """Find a single element by tag and class name"""
        return soup.find(tag, class_=class_name)

    @staticmethod
    def find_elements_by_tag_and_class(soup: BeautifulSoup, tag: str, class_name: str) -> List[Tag]:
        """Find multiple elements by tag and class name"""
        return soup.find_all(tag, class_=class_name)

    @staticmethod
    def get_text_content(element: Optional[Tag], selector: str) -> Optional[str]:
        """Get text content from an element using CSS selector"""
        found = HtmlParser.find_element(element, selector) if element else None
        return HtmlParser.get_text(found)

    @staticmethod
    def get_attribute_content(element: Optional[Tag], selector: str, attribute: str) -> Optional[str]:
        """Get attribute content from an element using CSS selector"""
        found = HtmlParser.find_element(element, selector) if element else None
        return HtmlParser.get_attribute(found, attribute) 