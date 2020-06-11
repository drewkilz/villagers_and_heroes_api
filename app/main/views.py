from flask import render_template, abort
from http import HTTPStatus

from . import main
from app.api.recipes import get_recipe, get_recipes
from app.crafting_calculator import calculate, CraftingOptions
from app.models.crafting_list import CraftingList
from app.models.schemas.recipe import RecipeSchema


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/credits')
def credits_():
    return render_template('credits.html')


@main.route('/equipment')
def equipment():
    return render_template('equipment.html')


@main.route('/recipes')
def recipes():
    response = get_recipes()

    if response.status_code == HTTPStatus.OK:
        schema = RecipeSchema()
        recipes_ = [schema.load(recipe) for recipe in response.json['recipes']]
    else:
        abort(HTTPStatus.INTERNAL_SERVER_ERROR)

    return render_template('recipes.html', recipes=recipes_)


@main.route('/crafting')
def crafting():
    from test import _40

    list_ = CraftingList()
    for recipe_name, quantity in _40:
        recipe = RecipeSchema().load(get_recipe(recipe_name))
        list_.add(recipe, quantity)

    calculate(list_, CraftingOptions(salvaging=True))

    return render_template('crafting.html', crafting_list=list_)
