from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy.fields import Nested

from app.models.category import Category
from app.models.schemas.type import TypeSchema


class CategorySchema(SQLAlchemySchema):
    class Meta:
        model = Category
        load_instance = True
        transient = True

    id = auto_field()
    name = auto_field()
    types = Nested(TypeSchema, many=True)
