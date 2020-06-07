from dataclasses import dataclass
from re import match
from typing import Any

from models.item import Item
from models.object import Object


@dataclass
class Ingredient(Object):
    item: Item
    quantity: int

    @classmethod
    def parse(cls, value: str, data: Any):
        match_ = match('^([0-9]+)(.+)$', value)

        if match_:
            quantity = int(match_[1])
            name = match_[2].strip()
        else:
            raise ValueError('Unable to parse ingredient quantity and name from: "{}"'.format(value))

        item = data.get_item(name)

        if item is None:
            raise ValueError('Unable to find item: "{}" from ingredient string: "{}"'.format(name, value))

        return Ingredient(item, quantity)
