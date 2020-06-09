from dataclasses import dataclass
from re import match

from app.data.object import Object


@dataclass
class Ingredient(Object):
    name: str
    quantity: int

    @classmethod
    def parse(cls, value: str):
        match_ = match('^([0-9]+)(.+)$', value)

        if match_:
            quantity = int(match_[1])
            name = match_[2].strip()
        else:
            raise ValueError('Unable to parse ingredient quantity and name from: "{}"'.format(value))

        return Ingredient(name, quantity)
