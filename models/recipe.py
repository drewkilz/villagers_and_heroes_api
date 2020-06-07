"""Contains classes and functionality pertaining to recipes for crafting items."""

from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict, Any

from models.class_ import Class
from models.ingredient import Ingredient
from models.object import Object
from models.skill import CraftingSkill
from models.type import CraftingType


@dataclass
class Recipe(Object):
    name: str
    skill: CraftingSkill
    type: CraftingType
    level: int
    ingredients: List[Ingredient]
    experience: int = None
    cost: Decimal = None
    class_: Class = None

    @classmethod
    def from_dict(cls, dictionary: Dict, data: Any):
        updated_dictionary = dictionary.copy()

        if 'skill' in dictionary:
            skill_string = dictionary['skill']
            if isinstance(skill_string, str):
                skill = CraftingSkill.find(skill_string)
                if skill is None:
                    raise ValueError('Unable to find CraftingSkill with name: "{}"'.format(skill_string))
                updated_dictionary['skill'] = skill

        if 'type' in dictionary:
            type_string = dictionary['type']
            if isinstance(type_string, str):
                try:
                    type_ = CraftingType(type_string)
                except ValueError:
                    raise ValueError('Unable to find CraftingType with name: "{}"'.format(type_string))
                updated_dictionary['type'] = type_

        if 'ingredients' in dictionary:
            ingredients_string = dictionary['ingredients']
            if isinstance(ingredients_string, str):
                ingredients = []

                for ingredient_string in [i.strip() for i in ingredients_string.split(',')]:
                    ingredients.append(Ingredient.parse(ingredient_string, data))

                updated_dictionary['ingredients'] = ingredients

        if 'class_' in dictionary:
            class_string = dictionary['class_']
            if isinstance(class_string, str):
                try:
                    class_ = Class(class_string)
                except ValueError:
                    raise ValueError('Unable to find Class with name: "{}"'.format(class_string))
                updated_dictionary['class_'] = class_

        return super().from_dict(updated_dictionary, data)
