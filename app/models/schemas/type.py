from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.models.type import Type


class TypeSchema(SQLAlchemySchema):
    class Meta:
        model = Type
        load_instance = True

    id = auto_field()
    category = auto_field()
    name = auto_field()
