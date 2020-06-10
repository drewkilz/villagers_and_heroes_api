from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from app.models.category import Category


class CategorySchema(SQLAlchemySchema):
    class Meta:
        model = Category
        load_instance = True

    id = auto_field()
    name = auto_field()
    types = auto_field()
