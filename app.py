from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from crafting_calculator import CraftingCalculator, CraftingOptions
from db import Data
from models.crafting_list import CraftingList

app = Flask(__name__)
bootstrap = Bootstrap(app)
data = Data()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/equipment')
def equipment():
    return render_template('equipment.html')


@app.route('/recipes')
def recipes():
    return render_template('recipes.html', recipes=data.all_recipes())


@app.route('/crafting')
def crafting():
    recipes_ = (("Golem's Firm Axe", 40),)

    list_ = CraftingList()
    for recipe_name, quantity in recipes_:
        list_.add(data.get_recipe(recipe_name), quantity)

    calculator = CraftingCalculator(data)
    calculator.calculate(list_, CraftingOptions(salvaging=True))

    return render_template('crafting.html', crafting_list=list_)


@app.errorhandler(404)
def page_not_found(e):
    raise ValueError('whhops')
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
