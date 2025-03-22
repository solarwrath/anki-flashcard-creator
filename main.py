import json
from pprint import pprint
from typing import List

from card_composers.composer_base import ComposerBase
from card_composers.composer_noun import ComposerNoun
from model.enums.word_category import WordCategory
from model.responses.response_base import Response
from model.variants.noun_variant import NounVariant
from model.variants.variant import Variant
from model.variants.variant_augmenter import NounVariantAugmenter, VariantAugmenter
from website_parsers.larousse_parser import LarousseParser
from website_parsers.linguee_parser import LingueeParser

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


def create_anki_card(query: str) -> Response:
    query = query.strip()

    # Create a single response with all variants
    response = Response()

    # Get all variants from Linguee
    linguee_parser = LingueeParser(query)
    variants = linguee_parser.get_variants()

    # Augment each variant with category-specific data
    for variant in variants:
        try:
            augmenter = create_variant_augmenter(variant, linguee_parser)
            augmenter.augment(variant)
        except NotImplementedError:
            # TODO: Support other word categories (verbs, adjectives, etc.)
            continue
        except ValueError as e:
            print(f"Warning: {e}")
            continue
    
    # Add variants to response
    response.variants.extend(variants)

    return response


def create_variant_augmenter(variant: Variant, linguee_parser: LingueeParser) -> VariantAugmenter:
    match variant.category:
        case WordCategory.noun:
            return NounVariantAugmenter(linguee_parser)
        case WordCategory.verb:
            # TODO: Implement VerbVariantAugmenter when ready
            raise NotImplementedError("Verb variants are not yet supported")
        case _:
            raise ValueError(f"No augmenter for such word category: {variant.category}")


if __name__ == '__main__':
    response = create_anki_card('livre')
    serialized_response = json.dumps(response.to_dict(), indent=2, ensure_ascii=False)
    print(serialized_response)