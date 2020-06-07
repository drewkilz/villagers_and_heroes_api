from db import Data
from models.recipes import Recipes


def test(recipes):
    data = Data()
    recipes_ = Recipes(data)
    for recipe_name, quantity in recipes:
        recipes_.add(data.get_recipe(recipe_name), quantity)
    recipes_.calculate(salvaging=True)
    recipes_.print()


if __name__ == '__main__':
    _30_34 = (
        ("Oread's Firm Axe", 40),
        ("Oread's Firm Armor", 40),
        ("Oread's Firm Belt", 40),
        ("Oread's Firm Gauntlets", 40),
        ("Oread's Firm Boots", 40),
        ("Oread's Helm", 40),
        ("Naiad's Calming Shield", 40),
        ("Wooden Raven Carving", 50)
    )

    _55_59 = (
        ("Golem's Firm Axe", 40),
        ("Golem's Firm Armor", 40),
        ("Golem's Firm Belt", 40),
        ("Golem's Firm Gauntlets", 40),
        ("Golem's Firm Boots", 40),
        ("Golem's Helm", 40),
        ("Selkie's Calming Shield", 40),
        ('Wooden Bullfrog Carving', 50)
    )

    _55_56 = (
        ("Golem's Helm", 40),
        ("Golem's Firm Armor", 40),
        ("Golem's Firm Axe", 40),
        ("Greater Scaline Dram of Mastery", 5)
    )

    test(_55_56)
