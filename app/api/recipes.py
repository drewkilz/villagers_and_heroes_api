from http import HTTPStatus

from flask import jsonify, request, current_app, url_for
from sqlalchemy import asc, desc
from sqlalchemy_filters import apply_filters

from app.api import api
from app.models.item import Item
from app.models.recipe import Recipe
from app.models.schemas.recipe import RecipeSchema
from app.models.type import Type
from configuration import ENV_VNH_RECIPES_PER_PAGE


@api.route('/recipes/<str_or_int:id_or_name>')
def get_recipe(id_or_name):
    if isinstance(id_or_name, int):
        filter_ = {'id': id_or_name}
    else:
        filter_ = {'name': id_or_name}

    recipe = Recipe.query.filter_by(**filter_).first()

    if recipe is None:
        # Returning no content as 404s are considered errors and cause logging on the UI side
        return '', HTTPStatus.NO_CONTENT

    return RecipeSchema().dump(recipe)


@api.route('/recipes/', methods=['GET', 'POST'])
def get_recipes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('perPage', current_app.config[ENV_VNH_RECIPES_PER_PAGE], type=int)
    sort_by = request.args.get('sortBy', 'name', type=str)
    sort_order = request.args.get('sortOrder', 'asc', type=str)
    sort_order_function = asc if sort_order == 'asc' else desc

    filter_ = None
    if request.json and 'filter' in request.json:
        filter_ = request.json['filter']

    query = Recipe.query

    if filter_:
        for current_filter in filter_:
            field = current_filter['field']
            if field in ('skill', 'type', 'class', 'subclass', 'rarity'):
                current_filter['field'] = '{}_id'.format(current_filter['field'])
                if field in ('class', 'subclass', 'rarity'):
                    current_filter['model'] = 'Item'

        query = apply_filters(query, filter_)

    if sort_by == 'name':
        query = query.order_by(sort_order_function(Recipe.name))
    elif sort_by == 'level':
        query = query.order_by(sort_order_function(Recipe.level))
    elif sort_by == 'skill':
        query = query.join(Recipe.skill).order_by(sort_order_function(Type.name))
    elif sort_by == 'type':
        query = query.join(Recipe.type).order_by(sort_order_function(Type.name))
    elif sort_by == 'class':
        query = query.join(Recipe.item).join(Item.class_).order_by(sort_order_function(Type.name))
    elif sort_by == 'subclass':
        query = query.join(Recipe.item).join(Item.subclass).order_by(sort_order_function(Type.name))

    pagination = query.paginate(page, per_page=per_page, error_out=False)

    recipes = pagination.items

    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_recipes', page=page-1)

    next_ = None
    if pagination.has_next:
        next_ = url_for('api.get_recipes', page=page+1)

    return jsonify({
        'recipes': [RecipeSchema().dump(recipe) for recipe in recipes],
        'prev': prev,
        'next': next_,
        'count': pagination.total
    })
