import os
from app import create_app, sql_alchemy
from app.data import Data
from app.models.category import Category
from app.models.enum import CategoryEnum, SkillType, VillageSkill, CraftingType, ItemType, Class, Rarity, \
    CraftingSkill, GatheringSkill
from app.models.ingredient import Ingredient
from app.models.item import Item
from app.models.recipe import Recipe
from app.models.schemas.category import CategorySchema
from app.models.schemas.ingredient import IngredientSchema
from app.models.schemas.item import ItemSchema
from app.models.schemas.recipe import RecipeSchema
from app.models.schemas.type import TypeSchema
from app.models.type import Type
from configuration import ENV_FLASK_CONFIGURATION, DEVELOPMENT_KEY
# Out of order to disable circular import errors
from app.api.authentication import Authenticator

app = create_app(os.getenv(ENV_FLASK_CONFIGURATION) or DEVELOPMENT_KEY)


@app.shell_context_processor
def make_shell_context():
    """
    When running "flask shell", the items here are automatically imported and available for use.

    :return: The dictionary of items to have available in the shell.
    """

    return dict(sql_alchemy=sql_alchemy, Item=Item, Recipe=Recipe, Ingredient=Ingredient, Type=Type, Category=Category,
                CategoryEnum=CategoryEnum, SkillType=SkillType, VillageSkill=VillageSkill, CraftingType=CraftingType,
                ItemType=ItemType, Class=Class, Rarity=Rarity, CraftingSkill=CraftingSkill,
                GatheringSkill=GatheringSkill, Data=Data, ItemSchema=ItemSchema, CategorySchema=CategorySchema,
                TypeSchema=TypeSchema, RecipeSchema=RecipeSchema, IngredientSchema=IngredientSchema,
                Authenticator=Authenticator)


if __name__ == '__main__':
    app.run()
