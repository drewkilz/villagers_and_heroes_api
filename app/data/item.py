from dataclasses import dataclass
from typing import Dict

from app.data.object import Object
from app.models.enum import ItemType, Class, Rarity, SubClass


@dataclass
class Item(Object):
    name: str
    type: ItemType
    level: int = None
    class_: Class = None
    subclass: SubClass = None
    rarity: Rarity = None

    @classmethod
    def from_dict(cls, dictionary: Dict):
        cls.convert('type', dictionary, ItemType)
        cls.convert('class', dictionary, Class, optional=True, output_key='class_')
        cls.convert('subclass', dictionary, SubClass, optional=True)
        cls.convert('rarity', dictionary, Rarity, optional=True, default=Rarity.COMMON)

        return super().from_dict(dictionary)
