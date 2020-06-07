from math import trunc, ceil
from typing import List, Tuple, Dict

from db import Data
from models.item import Item, SALVAGE_KIT
from models.object import Object
from models.recipe import Recipe


class Recipes(Object):
    list: List[Tuple[Recipe, int]]
    crafted: Dict[str, Tuple[Recipe, int]]
    items: Dict[str, Tuple[Item, int]]

    def __init__(self, data: Data):
        self.list = []
        self.crafted = {}
        self.items = {}
        self.cost = 0
        self.data = data

    def add(self, recipe: Recipe, quantity: int):
        self.list.append((recipe, quantity))

    def _calculate(self, recipe: Recipe, quantity: int, salvaging=False):
        quantity_ = quantity

        # Add salvage kits, as needed
        if salvaging and recipe.type.is_salvageable():
            if self.data.salvage_kit.name in self.items:
                self.items[self.data.salvage_kit.name] = (self.data.salvage_kit, quantity +
                                                          self.items[self.data.salvage_kit.name][1])
            else:
                self.items[self.data.salvage_kit.name] = (self.data.salvage_kit, quantity)

        for ingredient in recipe.ingredients:
            if salvaging and recipe.type.is_salvageable():
                if ingredient.item.type == 'Crafting Component':
                    # Roughly 20% are returned, so can reduce by that amount
                    quantity_ = ceil(quantity * 0.8)
                elif ingredient.item.type == 'Crafting Ingredient':
                    # Roughly 65% are returned, so can reduce by that amount
                    quantity_ = ceil(quantity * 0.35)

            sub_recipe = self.data.get_recipe(ingredient.item.name)
            if sub_recipe:
                self._calculate(sub_recipe, quantity_ * ingredient.quantity, salvaging=salvaging)
                if sub_recipe.name in self.crafted:
                    self.crafted[sub_recipe.name] = (sub_recipe, quantity_ * ingredient.quantity +
                                                     self.crafted[sub_recipe.name][1])
                else:
                    self.crafted[sub_recipe.name] = (sub_recipe, quantity_ * ingredient.quantity)
            else:
                if ingredient.item.name in self.items:
                    self.items[ingredient.item.name] = (ingredient.item, quantity_ * ingredient.quantity +
                                                        self.items[ingredient.item.name][1])
                else:
                    self.items[ingredient.item.name] = (ingredient.item, quantity_ * ingredient.quantity)

        self.cost += (recipe.cost * quantity)

    def calculate(self, salvaging=False):
        self.crafted = {}
        self.items = {}
        self.cost = 0

        for recipe, quantity in self.list:
            self._calculate(recipe, quantity, salvaging=salvaging)

    def print(self):
        print('Raw Materials')
        for name, (item, quantity) in self.items.items():
            if name == SALVAGE_KIT:
                stacks = quantity / 30.0
            else:
                stacks = quantity / item.stack_size
            print('\t{0: >5}   {1:>5.2}   {2}'.format(quantity, stacks, name))

        print()
        print('Crafted Materials')
        for name, (recipe, quantity) in self.crafted.items():
            print('\t{0: >5}   {1:>5.2}   {2}'.format(quantity, quantity / self.data.get_item(recipe.name).stack_size, name))

        print()
        print('Recipes')
        for recipe, quantity in self.list:
            print('\t{0: >5}   {1}'.format(quantity, recipe.name))

        print()
        print('Gold cost')
        gold = trunc(self.cost)
        silver = trunc(self.cost * 100 - gold * 100)
        copper = trunc(self.cost * 10000 - gold * 10000 - silver * 100)
        print('\t{} gp\t{} sp\t{} cp'.format(gold, silver, copper))
