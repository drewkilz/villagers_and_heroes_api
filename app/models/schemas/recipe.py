from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.models.recipe import Recipe


class RecipeSchema(SQLAlchemySchema):
    class Meta:
        model = Recipe
        load_instance = True

    id = auto_field()
    name = auto_field()
    type = auto_field()
    level = auto_field()
    cost = auto_field()
    item = auto_field()
    skill = auto_field()
    ingredients = auto_field()
