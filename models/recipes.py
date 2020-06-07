from math import trunc, ceil
from typing import List, Tuple, Dict

from db import Data
from models.item import Item, SALVAGE_KIT
from models.object import Object
from models.recipe import Recipe


class Recipes(Object):
    _list: List[Tuple[Recipe, int]]
    _crafted: Dict[str, Tuple[Recipe, int]]
    _items: Dict[str, Tuple[Item, int]]

    def __init__(self, data: Data):
        self._list = []
        self._crafted = {}
        self._items = {}
        self._cost = 0
        self._data = data

    def add(self, recipe: Recipe, quantity: int):
        self._list.append((recipe, quantity))

    def _calculate(self, recipe: Recipe, quantity: int, salvaging=False):
        quantity_ = quantity

        # Add salvage kits, as needed
        if salvaging and recipe.type.is_salvageable():
            if self._data.salvage_kit.name in self._items:
                self._items[self._data.salvage_kit.name] = (self._data.salvage_kit, quantity +
                                                            self._items[self._data.salvage_kit.name][1])
            else:
                self._items[self._data.salvage_kit.name] = (self._data.salvage_kit, quantity)

        for ingredient in recipe.ingredients:
            if salvaging and recipe.type.is_salvageable():
                if ingredient.item.type == 'Crafting Component':
                    # Roughly 20% are returned, so can reduce by that amount
                    quantity_ = ceil(quantity * 0.8)
                elif ingredient.item.type == 'Crafting Ingredient':
                    # Roughly 65% are returned, so can reduce by that amount
                    quantity_ = ceil(quantity * 0.35)

            sub_recipe = self._data.get_recipe(ingredient.item.name)
            if sub_recipe:
                self._calculate(sub_recipe, quantity_ * ingredient.quantity, salvaging=salvaging)
                if sub_recipe.name in self._crafted:
                    self._crafted[sub_recipe.name] = (sub_recipe, quantity_ * ingredient.quantity +
                                                      self._crafted[sub_recipe.name][1])
                else:
                    self._crafted[sub_recipe.name] = (sub_recipe, quantity_ * ingredient.quantity)
            else:
                if ingredient.item.name in self._items:
                    self._items[ingredient.item.name] = (ingredient.item, quantity_ * ingredient.quantity +
                                                         self._items[ingredient.item.name][1])
                else:
                    self._items[ingredient.item.name] = (ingredient.item, quantity_ * ingredient.quantity)

        self._cost += (recipe.cost * quantity)

    def calculate(self, salvaging=False):
        self._crafted = {}
        self._items = {}
        self._cost = 0

        for recipe, quantity in self._list:
            self._calculate(recipe, quantity, salvaging=salvaging)

    def print(self):
        print('Raw Materials')
        for name, (item, quantity) in self._items.items():
            if name == SALVAGE_KIT:
                stacks = quantity / 30.0
            else:
                stacks = quantity / item.stack_size
            print('\t{0: >5}   {1:>5.2}   {2}'.format(quantity, stacks, name))

        print()
        print('Crafted Materials')
        for name, (recipe, quantity) in self._crafted.items():
            print('\t{0: >5}   {1:>5.2}   {2}'.format(quantity, quantity / self._data.get_item(recipe.name).stack_size, name))

        print()
        print('Recipes')
        for recipe, quantity in self._list:
            print('\t{0: >5}   {1}'.format(quantity, recipe.name))

        print()
        print('Gold cost')
        gold = trunc(self._cost)
        silver = trunc(self._cost * 100 - gold * 100)
        copper = trunc(self._cost * 10000 - gold * 10000 - silver * 100)
        print('\t{} gp\t{} sp\t{} cp'.format(gold, silver, copper))
