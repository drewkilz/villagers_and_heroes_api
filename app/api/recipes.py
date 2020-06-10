from flask import jsonify, request, current_app, url_for, abort

from app.api import api
from app.models.recipe import Recipe
from app.models.schemas.recipe import RecipeSchema
from configuration import ENV_VNH_RECIPES_PER_PAGE


@api.route('/recipes/<str_or_int:id_or_name>')
def get_recipe(id_or_name):
    if isinstance(id_or_name, int):
        filter_ = {'id': id_or_name}
    else:
        filter_ = {'name': id_or_name}

    recipe = Recipe.query.filter_by(**filter_).first()

    if recipe is None:
        abort(404)

    return RecipeSchema().dump(recipe)


@api.route('/recipes/')
def get_recipes():
    page = request.args.get('page', 1, type=int)

    pagination = Recipe.query.order_by(Recipe.name.asc()).paginate(
        page, per_page=current_app.config[ENV_VNH_RECIPES_PER_PAGE],
        error_out=False)

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
