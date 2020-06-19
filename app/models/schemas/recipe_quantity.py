from marshmallow import Schema, fields

from app.models.schemas.quantity import QuantitySchema
from app.models.schemas.recipe import RecipeSchema


class RecipeQuantityInputSchema(Schema):
    recipe = fields.Integer(required=True)
    quantity = fields.Integer(missing=1)


class RecipeQuantityOutputSchema(RecipeSchema, QuantitySchema):
    pass
