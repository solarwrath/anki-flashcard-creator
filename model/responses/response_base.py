from model.ConfiguredPydanticBaseModel import ConfiguredPydanticBaseModel
from model.enums.word_category import WordCategory


class Response(ConfiguredPydanticBaseModel):
    category: WordCategory
    pronunciation: str | None = None
    image: str | None = None
    english_definition: str