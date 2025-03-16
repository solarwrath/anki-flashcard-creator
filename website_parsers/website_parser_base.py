from typing import Any
import abc

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from model.ConfiguredPydanticBaseModel import ConfiguredPydanticBaseModel


class WebsiteParserBase(ConfiguredPydanticBaseModel, metaclass=abc.ABCMeta):
    query: str | None
    soup: BeautifulSoup | None


    def __init__(self, query):
        super().__init__()  # Use parent __init__
        self.query = query
        self.soup = self.query_dictionary()


    @abc.abstractmethod
    def compose_query_url(self)->str:
        pass


    def query_dictionary(self)->BeautifulSoup:
        url = self.compose_query_url()
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")