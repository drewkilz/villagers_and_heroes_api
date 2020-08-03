from typing import TYPE_CHECKING

from app import sql_alchemy
from app.models.ingredient import Ingredient
from app.models.item import Item
from app.models.load import LoadMixin
from app.models.quantity import QuantityMixin
from app.models.enum import CategoryEnum

if TYPE_CHECKING:
    from app.data import Recipe as DataRecipe


class Recipe(sql_alchemy.Model, QuantityMixin, LoadMixin):
    __tablename__ = 'recipes'

    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True, nullable=False)
    name = sql_alchemy.Column(sql_alchemy.Unicode(255), unique=True, index=True, nullable=False)
    type_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=False)
    level = sql_alchemy.Column(sql_alchemy.SmallInteger, nullable=False)
    cost = sql_alchemy.Column(sql_alchemy.Numeric(precision=7, scale=4), nullable=False)
    item_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('items.id'), nullable=False)
    skill_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=False)

    type = sql_alchemy.relationship('Type', foreign_keys=[type_id])
    item = sql_alchemy.relationship('Item')
    skill = sql_alchemy.relationship('Type', foreign_keys=[skill_id])

    ingredients = sql_alchemy.relationship('Ingredient', backref='ingredients', lazy='dynamic')

    def __repr__(self):
        return 'Recipe(id={}, name={}, skill={}, type={}, level={}, cost={}, item={})'.format(
            self.id, self.name, self.skill, self.type, self.level, self.cost, self.item)

    @classmethod
    def load(cls, data: 'DataRecipe'):
        recipe = Recipe(
            name=data.name,
            type=cls.get_type(data.type, CategoryEnum.CRAFTING_TYPE),
            level=data.level,
            cost=data.cost,
            item=Item.query.filter_by(name=data.name).first(),
            skill=cls.get_type(data.skill, CategoryEnum.SKILL))

        recipe.ingredients = []
        for ingredient_data in data.ingredients:
            ingredient = Ingredient(
                recipe=recipe,
                item=Item.query.filter_by(name=ingredient_data.name).first(),
                quantity=ingredient_data.quantity)
            recipe.ingredients.append(ingredient)

        sql_alchemy.session.add(recipe)
