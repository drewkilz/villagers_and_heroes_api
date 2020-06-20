from flask import jsonify, abort

from app.api import api
from app.models.category import Category
from app.models.schemas.category import CategorySchema


@api.route('/categories/<str_or_int:id_or_name>')
def get_category(id_or_name):
    if isinstance(id_or_name, int):
        filter_ = {'id': id_or_name}
    else:
        filter_ = {'name': id_or_name}

    category = Category.query.filter_by(**filter_).first()

    if category is None:
        abort(404)

    return CategorySchema().dump(category)


@api.route('/categories/')
def get_categories():
    categories = Category.query.all()

    return jsonify({
        'categories': CategorySchema(many=True).dump(categories)
    })
