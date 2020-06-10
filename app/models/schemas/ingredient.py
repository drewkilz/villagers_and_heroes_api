from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.models.ingredient import Ingredient


class IngredientSchema(SQLAlchemySchema):
    class Meta:
        model = Ingredient
        load_instance = True

    recipe = auto_field()
    item = auto_field()
    quantity = auto_field()
