from marshmallow import Schema, fields
from marshmallow.fields import Nested

from app.models.schemas.item_quantity import ItemQuantityOutputSchema
from app.models.schemas.recipe_quantity import RecipeQuantityOutputSchema


class CraftingListSchema(Schema):
    list = fields.Dict(keys=fields.Str(), values=Nested(RecipeQuantityOutputSchema))
    components = fields.Dict(keys=fields.Str(), values=Nested(RecipeQuantityOutputSchema))
    refined = fields.Dict(keys=fields.Str(), values=Nested(RecipeQuantityOutputSchema))
    items = fields.Dict(keys=fields.Str(), values=Nested(ItemQuantityOutputSchema))
    cost = fields.Decimal()
