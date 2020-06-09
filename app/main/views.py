from flask import render_template

from . import main
from app.crafting_calculator import calculate, CraftingOptions
from app.models.crafting_list import CraftingList
from app.models.recipe import Recipe


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/equipment')
def equipment():
    return render_template('equipment.html')


@main.route('/recipes')
def recipes():
    return render_template('recipes.html', recipes=Recipe.query.all())


@main.route('/crafting')
def crafting():
    from test import _40

    list_ = CraftingList()
    for recipe_name, quantity in _40:
        list_.add(Recipe.query.filter_by(name=recipe_name).first(), quantity)

    calculate(list_, CraftingOptions(salvaging=True))

    return render_template('crafting.html', crafting_list=list_)
