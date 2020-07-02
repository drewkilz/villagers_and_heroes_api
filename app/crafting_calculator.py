from dataclasses import dataclass
from math import ceil

from app.models.crafting_list import CraftingList
from app.models.enum import CraftingType, ItemType
from app.models.item import SALVAGE_KIT, Item
from app.models.recipe import Recipe


@dataclass
class CraftingOptions:
    salvaging: bool = False

    # Default to 65% of Crafting Ingredients being returned during salvaging
    ingredient_salvage_percent: float = 0.65

    # Default to 20% of Crafting Components being returned during salvaging
    component_salvage_percent: float = 0.2


def _calculate(list_: CraftingList, recipe: Recipe, quantity: int, options: CraftingOptions):
    quantity_ = quantity

    # Add salvage kits, as needed
    if options.salvaging and recipe.item.salvageable:
        if SALVAGE_KIT not in list_.items:
            list_.items[SALVAGE_KIT] = Item.query.filter_by(name=SALVAGE_KIT).first()

        list_.items[SALVAGE_KIT].quantity += quantity

    for ingredient in recipe.ingredients:
        # Modify the quantity needed based on salvaged materials
        if options.salvaging and recipe.item.salvageable:
            if ingredient.item.type.name == ItemType.COMPONENT.value:
                quantity_ = ceil(quantity * (1 - options.component_salvage_percent))
            elif ingredient.item.type.name == ItemType.INGREDIENT.value:
                quantity_ = ceil(quantity * (1 - options.ingredient_salvage_percent))

        sub_recipe = Recipe.query.filter_by(name=ingredient.item.name).first()
        if sub_recipe:
            # Calculate the sub recipe
            _calculate(list_, sub_recipe, quantity_ * ingredient.quantity, options)

            if sub_recipe.type.name == CraftingType.REFINED.value:
                current_list = list_.refined
            elif sub_recipe.type.name == CraftingType.COMPONENT.value:
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
        if key not in current_list:
            current_list[key] = object_

        current_list[key].quantity += quantity_ * ingredient.quantity

    list_.cost += (recipe.cost * quantity)


def calculate(list_: CraftingList, options: CraftingOptions):
    list_.reset()

    for object_ in list_.list.values():
        _calculate(list_, object_, object_.quantity, options)
