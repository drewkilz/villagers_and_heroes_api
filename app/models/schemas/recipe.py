from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.recipe import Recipe
from app.models.schemas.ingredient import IngredientSchema
from app.models.schemas.item import ItemSchema
from app.models.schemas.type import TypeSchema


class RecipeSchema(SQLAlchemySchema):
    class Meta:
        model = Recipe
        load_instance = True
        transient = True

    id = auto_field()
    name = auto_field()
    type = Nested(TypeSchema)
    level = auto_field()
    cost = auto_field()
    item = Nested(ItemSchema)
    skill = Nested(TypeSchema)
    ingredients = Nested(IngredientSchema, many=True)
