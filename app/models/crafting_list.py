from typing import Dict

from app.models.cost import Cost
from app.models.item import Item
from app.models.recipe import Recipe


class CraftingList:
    list: Dict[str, Recipe] = {}
    components: Dict[str, Recipe] = {}
    refined: Dict[str, Recipe] = {}
    items: Dict[str, Item] = {}
    cost: Cost = Cost()

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
        self.cost = Cost()
