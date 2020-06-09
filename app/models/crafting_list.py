from math import trunc
from typing import Dict

from app.models.quantity import QuantityMixin
from app.models.recipe import Recipe


class CraftingList:
    list: Dict[str, Recipe] = {}
    components: Dict[str, QuantityMixin] = {}
    refined: Dict[str, QuantityMixin] = {}
    items: Dict[str, QuantityMixin] = {}
    cost: int = 0

    def __init__(self):
        self.reset(list_=True)

    def add(self, recipe: Recipe, quantity: int):
        if recipe.name not in self.list:
            self.list[recipe.name] = recipe

        self.list[recipe.name].quantity += quantity

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
