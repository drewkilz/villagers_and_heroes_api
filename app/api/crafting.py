from flask import jsonify, request, current_app, url_for, abort
from werkzeug.exceptions import NotFound

from app.api import api
from app.api.recipes import get_recipe
from app.crafting_calculator import calculate, CraftingOptions
from app.models.crafting_list import CraftingList
from app.models.schemas.crafting_list import CraftingListSchema
from app.models.schemas.recipe import RecipeSchema
from app.models.schemas.recipe_quantity import RecipeQuantityInputSchema


@api.route('/crafting_list/', methods=['POST'])
def crafting_list():
    recipe_quantities = RecipeQuantityInputSchema(many=True).loads(request.data)

    list_ = CraftingList()
    for recipe_quantity in recipe_quantities:
        recipe_json = None
        recipe_id = recipe_quantity['recipe']
        try:
            recipe_json = get_recipe(recipe_id)
        except NotFound:
            abort(404, description='Unable to locate recipe with id: {}'.format(recipe_id))

        recipe = RecipeSchema().load(recipe_json)

        list_.add(recipe, recipe_quantity['quantity'])

    calculate(list_, CraftingOptions(salvaging=True))

    return CraftingListSchema().dump(list_)


# @api.route('/recipes/<str_or_int:id_or_name>')
# def get_recipe(id_or_name):
#     if isinstance(id_or_name, int):
#         filter_ = {'id': id_or_name}
#     else:
#         filter_ = {'name': id_or_name}
#
#     recipe = Recipe.query.filter_by(**filter_).first()
#
#     if recipe is None:
#         abort(404)
#
#     return RecipeSchema().dump(recipe)
#
#
# @api.route('/recipes/')
# def get_recipes():
#     page = request.args.get('page', 1, type=int)
#
#     pagination = Recipe.query.order_by(Recipe.name.asc()).paginate(
#         page, per_page=current_app.config[ENV_VNH_RECIPES_PER_PAGE],
#         error_out=False)
#
#     recipes = pagination.items
#
#     prev = None
#     if pagination.has_prev:
#         prev = url_for('api.get_recipes', page=page-1)
#
#     next_ = None
#     if pagination.has_next:
#         next_ = url_for('api.get_recipes', page=page+1)
#
#     return jsonify({
#         'recipes': [RecipeSchema().dump(recipe) for recipe in recipes],
#         'prev': prev,
#         'next': next_,
#         'count': pagination.total
#     })
