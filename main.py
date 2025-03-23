import json

from model.response import Response
from logic.variant_augmenters import create_variant_augmenter
from logic.parsing.websites.linguee_parser import LingueeParser

"""
TODO: 
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
            augmenter = create_variant_augmenter(variant.category)
            augmenter.linguee_parser = linguee_parser  # Set the parser after creation
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


if __name__ == '__main__':
    response = create_anki_card('sans')
    serialized_response = json.dumps(response.to_dict(), indent=2, ensure_ascii=False)
    print(serialized_response)