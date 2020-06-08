from dataclasses import dataclass

from .object import Object

SALVAGE_KIT = 'Salvage Kit'


@dataclass
class Item(Object):
    name: str
    type: str
    level: int = None
    description: str = None

    @property
    def stack_size(self):
        if self.type.startswith('Natural'):
            return 350
        elif 'Crafting Ingredient' in self.type:
            return 350
        elif 'Crafting Component' in self.type:
            return 50
        elif self.name == 'Water':
            return 1000
        else:
            return None
