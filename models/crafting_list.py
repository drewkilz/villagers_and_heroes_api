from math import trunc
from typing import Dict

from models.object import Object
from models.object_quantity import ObjectQuantity
from models.recipe import Recipe


class CraftingList(Object):
    list: Dict[str, ObjectQuantity] = {}
    components: Dict[str, ObjectQuantity] = {}
    refined: Dict[str, ObjectQuantity] = {}
    items: Dict[str, ObjectQuantity] = {}
    cost: int = 0

    def add(self, recipe: Recipe, quantity: int):
        self.list[recipe.name] = ObjectQuantity(recipe, quantity)

    def reset(self, list_=False):
        if list_:
            self.list = {}

        self.components = {}
        self.refined = {}
        self.items = {}
        self.cost = 0

    @property
    def gold_pieces(self):
        return trunc(self.cost)

    @property
    def silver_pieces(self):
        return trunc(self.cost * 100 - self.gold_pieces * 100)

    @property
    def copper_pieces(self):
        return trunc(self.cost * 10000 - self.gold_pieces * 10000 - self.silver_pieces * 100)
