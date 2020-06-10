from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.item import Item
from app.models.schemas.type import TypeSchema


class ItemSchema(SQLAlchemySchema):
    class Meta:
        model = Item
        load_instance = True
        transient = True

    id = auto_field()
    name = auto_field()
    type = Nested(TypeSchema)
    level = auto_field(allow_none=True)
    class_ = Nested(TypeSchema, allow_none=True)
    subclass = Nested(TypeSchema, allow_none=True)
    rarity = Nested(TypeSchema)
