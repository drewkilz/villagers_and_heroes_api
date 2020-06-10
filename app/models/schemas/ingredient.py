from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.ingredient import Ingredient
from app.models.schemas.item import ItemSchema


class IngredientSchema(SQLAlchemySchema):
    class Meta:
        model = Ingredient
        load_instance = True
        transient = True

    item = Nested(ItemSchema)
    quantity = auto_field()
