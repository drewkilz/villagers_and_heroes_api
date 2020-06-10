from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.models.item import Item


class ItemSchema(SQLAlchemySchema):
    class Meta:
        model = Item
        load_instance = True

    id = auto_field()
    name = auto_field()
    type = auto_field()
    level = auto_field()
    class_ = auto_field()
    subclass = auto_field()
    rarity = auto_field()
