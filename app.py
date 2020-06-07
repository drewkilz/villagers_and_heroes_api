from math import trunc

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from db import Data
from models.item import SALVAGE_KIT
from models.recipes import Recipes

app = Flask(__name__)
bootstrap = Bootstrap(app)
data = Data()


@app.route('/')
def index():
    return """
    <a href="calculator">Calculator</a><br/>
    <a href="equipment">Equipment</a><br/>
    <a href="recipes">Recipes</a><br/>
"""


@app.route('/equipment')
def equipment():
    return """
<table>
    <tr>
        <th></th>
        <th>1</th>
        <th>2</th>
        <th>3</th>
        <th>4</th>
        <th>5</th>
        <th>6</th>
    </tr>
    <tr>
        <th>Weapon</th>
        <td>
            Kobold's Axe<br/>
            Merrow's Axe
        </td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>
            Kobold's Firm Axe<br/>
            Merrow's Calming Axe
        </td>
    </tr>
    <tr>
        <th>Shield</th>
        <td></td>
        <td>
            Kobold's Shield<br/>
            Merrow's Shield
        </td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>Armor</th>
        <td></td>
        <td>
            Kobold's Armor<br/>
            Merrow's Armor
        </td>
        <td></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <th>...</th>
        <td></td>
        <td></td>
        <td>...</td>
        <td></td>
        <td></td>
    </tr>
</table>"""


@app.route('/recipes')
def recipes():
    return render_template('recipes.html', recipes=data.all_recipes())


@app.route('/calculator')
def calculator():
    recipes_to_calculate = (("Golem's Firm Axe", 40),)
    recipes_ = Recipes(data)
    for recipe_name, quantity in recipes_to_calculate:
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
