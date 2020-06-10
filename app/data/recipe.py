from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List

from app.data.ingredient import Ingredient
from app.data.object import Object
from app.models.enum import CraftingType, CraftingSkill


@dataclass
class Recipe(Object):
    name: str
    skill: CraftingSkill
    type: CraftingType
    level: int
    ingredients: List[Ingredient]
    cost: Decimal = None

    @classmethod
    def from_dict(cls, dictionary: Dict):
        cls.convert('skill', dictionary, CraftingSkill)
        cls.convert('type', dictionary, CraftingType)

        if 'ingredients' in dictionary:
            ingredients_string = dictionary['ingredients']
            if isinstance(ingredients_string, str):
                ingredients = []
                for ingredient_string in [i.strip() for i in ingredients_string.split(',')]:
                    ingredients.append(Ingredient.parse(ingredient_string))
                dictionary['ingredients'] = ingredients

        return super().from_dict(dictionary)
