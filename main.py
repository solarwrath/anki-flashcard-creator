from pprint import pprint

from card_composers.composer_base import ComposerBase
from card_composers.composer_noun import ComposerNoun
from model.enums.word_category import WordCategory
from model.responses.response_base import Response
from website_parsers.larousse_parser import LarousseParser

"""
TODO: 
2. Implement getting image.
3. Implement getting English Meaning.
4. Implement getting examples.
5. Implement getting transcription.
6. Implement getting prononciation.
7. Implement getting "conjugates with"
8. Implement getting "conjugates as"
"""


def create_anki_card(query: str)->Response:
    query = query.strip()

    larousse_parser = LarousseParser(query)
    word_category = larousse_parser.get_word_category()

    composer = create_composer(word_category, query)

    return composer.compose()


def create_composer(word_category: WordCategory, query: str)->ComposerBase:
    match word_category:
        case WordCategory.noun:
            return ComposerNoun(query)
        case WordCategory.verb:
            return ComposerNoun(query)

    raise Exception(f"No composer for such word category: {word_category}")


if __name__ == '__main__':
    response = create_anki_card('livre')
    serialized_response = response.model_dump_json()
    pprint(serialized_response)
    #create_anki_card('manuel')