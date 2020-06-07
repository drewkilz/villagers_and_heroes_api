from math import trunc

from flask import Flask

from db import Data
from models.item import SALVAGE_KIT
from models.recipes import Recipes

app = Flask(__name__)


@app.route('/')
def index():
    recipes = (("Golem's Firm Axe", 40),)
    data = Data()
    recipes_ = Recipes(data)
    for recipe_name, quantity in recipes:
        recipes_.add(data.get_recipe(recipe_name), quantity)
    recipes_.calculate(salvaging=True)

    value = 'Raw Materials<br />'
    for name, (item, quantity) in recipes_.items.items():
        if name == SALVAGE_KIT:
            stacks = quantity / 30.0
        else:
            stacks = quantity / item.stack_size
        value += '\t{0: >5}   {1:>5.2}   {2}<br />'.format(quantity, stacks, name)

    value += '<br />'
    value += 'Crafted Materials<br />'
    for name, (recipe, quantity) in recipes_.crafted.items():
        value += '\t{0: >5}   {1:>5.2}   {2}<br />'.format(quantity, quantity / recipes_.data.get_item(recipe.name).stack_size, name)

    value += '<br />'
    value += 'Recipes<br />'
    for recipe, quantity in recipes_.list:
        value += '\t{0: >5}   {1}<br />'.format(quantity, recipe.name)

    value += '<br />'
    value += 'Gold cost<br />'
    gold = trunc(recipes_.cost)
    silver = trunc(recipes_.cost * 100 - gold * 100)
    copper = trunc(recipes_.cost * 10000 - gold * 10000 - silver * 100)
    value += '\t{} gp\t{} sp\t{} cp'.format(gold, silver, copper)

    return value


if __name__ == '__main__':
    app.run()
