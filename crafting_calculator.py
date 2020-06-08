from dataclasses import dataclass
from math import ceil

from db import Data
from models.crafting_list import CraftingList
from models.object_quantity import ObjectQuantity
from models.recipe import Recipe
from models.type import CraftingType


@dataclass
class CraftingOptions:
    salvaging: bool = False

    # Default to 65% of Crafting Ingredients being returned during salvaging
    ingredient_salvage_percent: float = 0.65

    # Default to 20% of Crafting Components being returned during salvaging
    component_salvage_percent: float = 0.2


class CraftingCalculator:
    def __init__(self, data: Data):
        self.data = data

    def _calculate(self, list_: CraftingList, recipe: Recipe, quantity: int, options: CraftingOptions):
        quantity_ = quantity

        # Add salvage kits, as needed
        if options.salvaging and recipe.type.is_salvageable():
            if self.data.salvage_kit.name in list_.items:
                list_.items[self.data.salvage_kit.name].quantity += quantity
            else:
                list_.items[self.data.salvage_kit.name] = ObjectQuantity(self.data.salvage_kit, quantity)

        # Look up the item for the recipe for usage in the UI
        recipe.item = self.data.get_item(recipe.name)

        for ingredient in recipe.ingredients:
            # Modify the quantity needed based on salvaged materials
            if options.salvaging and recipe.type.is_salvageable():
                if ingredient.item.type == 'Crafting Component':
                    quantity_ = ceil(quantity * (1 - options.component_salvage_percent))
                elif ingredient.item.type == 'Crafting Ingredient':
                    quantity_ = ceil(quantity * (1 - options.ingredient_salvage_percent))

            sub_recipe = self.data.get_recipe(ingredient.item.name)
            if sub_recipe:
                # Calculate the sub recipe
                self._calculate(list_, sub_recipe, quantity_ * ingredient.quantity, options)

                if sub_recipe.type == CraftingType.REFINED:
                    current_list = list_.refined
                elif sub_recipe.type == CraftingType.COMPONENTS:
                    current_list = list_.components
                else:
                    raise ValueError(
                        'Invalid crafting type: "{}" for a sub-recipe: "{}"'.format(sub_recipe.type, sub_recipe))

                key = sub_recipe.name
                object_ = sub_recipe
            else:
                # Just an item, not a recipe
                current_list = list_.items
                key = ingredient.item.name
                object_ = ingredient.item

            # Add the sub recipe to the crafting list
            if key in current_list:
                current_list[key].quantity += quantity_ * ingredient.quantity
            else:
                current_list[key] = ObjectQuantity(object_, quantity_ * ingredient.quantity)

        list_.cost += (recipe.cost * quantity)

    def calculate(self, list_: CraftingList, options: CraftingOptions):
        list_.reset()

        for object_ in list_.list.values():
            self._calculate(list_, object_.object, object_.quantity, options)
