from flask import render_template

from . import main
from .. import data
from ..crafting_calculator import CraftingCalculator, CraftingOptions
from ..models.crafting_list import CraftingList


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/equipment')
def equipment():
    return render_template('equipment.html')


@main.route('/recipes')
def recipes():
    return render_template('recipes.html', recipes=data.all_recipes())


@main.route('/crafting')
def crafting():
    from test import _40

    list_ = CraftingList()
    for recipe_name, quantity in _40:
        list_.add(data.get_recipe(recipe_name), quantity)

    calculator = CraftingCalculator(data)
    calculator.calculate(list_, CraftingOptions(salvaging=True))

    return render_template('crafting.html', crafting_list=list_)
