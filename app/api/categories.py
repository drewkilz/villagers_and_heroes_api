from http import HTTPStatus

from flask import jsonify, abort
from sqlalchemy_filters import apply_filters

from app.api import api
from app.models.category import Category
from app.models.enum import CraftingSkill, GatheringSkill, VillageSkill
from app.models.schemas.category import CategorySchema
from app.models.schemas.type import TypeSchema
from app.models.type import Type


@api.route('/categories/<str_or_int:id_or_name>')
def get_category(id_or_name):
    if isinstance(id_or_name, int):
        filter_ = {'id': id_or_name}
    else:
        filter_ = {'name': id_or_name}

    category = Category.query.filter_by(**filter_).first()

    if category is None:
        # Returning no content as 404s are considered errors and cause logging on the UI side
        return '', HTTPStatus.NO_CONTENT

    return CategorySchema().dump(category)


@api.route('/categories/')
def get_categories():
    categories = Category.query.all()

    return jsonify({
        'categories': CategorySchema(many=True).dump(categories)
    })


@api.route('/skills/<name>')
def get_skills(name):
    if name == 'Crafting':
        enum = CraftingSkill
    elif name == 'Gathering':
        enum = GatheringSkill
    elif name == 'Village':
        enum = VillageSkill
    else:
        # Returning no content as 404s are considered errors and cause logging on the UI side
        return '', HTTPStatus.NO_CONTENT

    skill_names = []

    for skill in enum:
        skill_names.append(skill.value)

    filter_spec = [
        {'field': 'category_id', 'op': 'eq', 'value': Category.query.filter_by(name='Skill').one().id},
        {'field': 'name', 'op': 'in', 'value': skill_names},
    ]

    types = apply_filters(Type.query, filter_spec).all()

    return jsonify({
        'types': TypeSchema(many=True).dump(types)
    })
