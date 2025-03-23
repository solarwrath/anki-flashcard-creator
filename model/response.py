from typing import List

from model.variants.variant import Variant


class Response:
    variants: List[Variant]

    def __init__(self):
        self.variants = []

    def to_dict(self):
        return {
            'variants': [variant.to_dict() for variant in self.variants]
        }