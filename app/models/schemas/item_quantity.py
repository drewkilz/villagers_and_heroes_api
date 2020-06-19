from app.models.schemas.item import ItemSchema
from app.models.schemas.quantity import QuantitySchema


class ItemQuantityOutputSchema(ItemSchema, QuantitySchema):
    pass
