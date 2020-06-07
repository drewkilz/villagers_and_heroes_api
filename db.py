"""Contains the data related to Villagers and Heroes."""

from csv import DictReader
from dataclasses import fields
from typing import Type, Dict, Any

from dacite.exceptions import MissingValueError

from models.item import Item, SALVAGE_KIT
from models.object import Object
from models.recipe import Recipe


class Data:
    _items: Dict[str, Item] = {}
    _recipes: Dict[str, Recipe] = {}
    _salvage_kit: Item = None

    def __init__(self):
        self._items = self.__get_data(r'data/items.csv', Item, 'name')
        self._recipes = self.__get_data(r'data/recipes.csv', Recipe, 'name')

    def __get_data(self, file_path: str, class_: Type[Object], key: str) -> Dict[str, Any]:
        objects = {}

        if key not in [field.name for field in fields(class_)]:
            raise ValueError('Key specified: "{}" does not exist in class: "{}".'.format(key, class_.__name__))

        with open(file_path, encoding='utf-8-sig') as file:
            reader = DictReader(file)
            for line_number, row in enumerate(reader):
                try:
                    object_ = class_.from_dict(row, self)
                except MissingValueError:
                    raise ValueError('Failed to retrieve data from file: "{}", line: "{}"'.format(
                        file_path, line_number + 1))

                objects[getattr(object_, key)] = object_

        return objects

    def _get_item(self, name):
        item = self.get_item(name)
        if item:
            return item

        raise ValueError('No item with name: {}.'.format(name))

    def get_item(self, name):
        if name in self._items:
            return self._items[name]

        return None

    def get_recipe(self, name):
        if name in self._recipes:
            return self._recipes[name]

        return None

    @property
    def salvage_kit(self):
        if self._salvage_kit is None:
            self._salvage_kit = self.get_item(SALVAGE_KIT)

        return self._salvage_kit
