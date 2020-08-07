from typing import Union, List

from flask import jsonify, request
from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_

from app.api import api
from app.api.errors import bad_request
from app.models.category import Category
from app.models.enum import CraftingType, CategoryEnum, VillagerClass
from app.models.item import Item
from app.models.recipe import Recipe
from app.models.schemas.recipe import RecipeSchema
from app.models.type import Type


@api.route('/equipment/')
def get_equipment():
    level = request.args.get('level', None, type=int)
    num_levels = request.args.get('numLevels', None, type=int)
    hero_class = request.args.getlist('heroClass', type=int)
    hero_sub_class = request.args.getlist('heroSubClass', type=int)
    villager_class = request.args.getlist('villagerClass', type=int)

    if level is None:
        return bad_request('Missing argument: level')
    if num_levels is None:
        return bad_request('Missing argument: numLevels')
    if not hero_class and not hero_sub_class and not villager_class:
        return bad_request('Missing argument: heroClass, heroSubClass, or villagerClass')

    data = {}

    if hero_class or hero_sub_class:
        class_query = None
        if hero_class:
            class_query = Recipe.query.join(Recipe.item).filter(Item.class_id.in_(hero_class))
        if hero_sub_class:
            class_query = class_query.join(Recipe.item).filter(Item.subclass_id.in_(hero_sub_class)) if class_query \
                else Recipe.query.join(Recipe.item).filter(Item.subclass_id.in_(hero_sub_class))

        # Hero Class / Sub-Class Equipment
        _add_data(data, class_query, CraftingType.ARMOR, level, num_levels)
        _add_data(data, class_query,
                  [CraftingType.AXE, CraftingType.BOW, CraftingType.MACE, CraftingType.STAFF, CraftingType.SWORD],
                  level, num_levels, key='Weapon')
        _add_data(data, class_query, CraftingType.SHIELD, level, num_levels)
        _add_data(data, class_query, CraftingType.BELT, level, num_levels)
        _add_data(data, class_query, CraftingType.GLOVE, level, num_levels)
        _add_data(data, class_query, CraftingType.BOOTS, level, num_levels)
        _add_data(data, class_query, CraftingType.HATS, level, num_levels)
        
        _add_data(data, Recipe.query, CraftingType.TRINKET, level, num_levels)

        # Preparations
        _add_data(data, Recipe.query, CraftingType.POWDER, level, num_levels)
        _add_data(data, Recipe.query, CraftingType.EMBROIDERY, level, num_levels)
        _add_data(data, Recipe.query, CraftingType.RESIN, level, num_levels)

        # Consumables
        _add_data(data, Recipe.query.filter(Recipe.name.like('% Mana Roll')), CraftingType.FOOD, level, num_levels,
                  key='Mana Roll')
        _add_data(data, Recipe.query.filter(Recipe.name.like('% Fish %')), CraftingType.FOOD, level, num_levels,
                  key='Fish Dinner')
        _add_data(data, Recipe.query.filter(or_(Recipe.name.like('% Breakfast'), Recipe.name.like('% Brunch'))),
                  CraftingType.FOOD, level, num_levels, key='Breakfast')
        _add_data(data, Recipe.query, CraftingType.DRAM, level, num_levels)
        _add_data(data, Recipe.query, CraftingType.MANA, level, num_levels)
        _add_data(data, Recipe.query, CraftingType.HEALTH, level, num_levels)

    # Consumables for both heroes and villagers
    _add_data(data, Recipe.query.filter(Recipe.name.like('% Pie')), CraftingType.FOOD, level, num_levels, key='Pie')
    _add_data(data, Recipe.query, CraftingType.TRIAD, level, num_levels)

    if villager_class:
        # Convert villager class to skills
        villager_class_skills = []
        for current_villager_class in villager_class:
            villager_class_type = Type.query.filter_by(id=current_villager_class,
                                                       category=Category.query.filter_by(
                                                           name=CategoryEnum.VILLAGER_CLASS.value).first()).first()
            villager_class_ = VillagerClass(villager_class_type.name)
            skill = villager_class_.get_crafting_skill()
            villager_class_skills.append(Type.query.filter_by(name=skill.value,
                                                              category=Category.query.filter_by(
                                                                  name=CategoryEnum.SKILL.value).first()).first())

        villager_query = Recipe.query.filter(Recipe.skill_id.in_(
            [villager_class_skill.id for villager_class_skill in villager_class_skills]))

        # Villager Class Equipment
        _add_data(data, villager_query, CraftingType.TOOL, level, num_levels)
        _add_data(data, villager_query, CraftingType.NECKLACE, level, num_levels)
        _add_data(data, villager_query.filter(Recipe.name.in_([
            VillagerClass.CARPENTER.get_special_recipe(),
            VillagerClass.CHEF.get_special_recipe(),
            VillagerClass.SMITH.get_special_recipe(),
            VillagerClass.TAILOR.get_special_recipe()]
        )), CraftingType.SPECIAL, level, num_levels, key='Villager Special')

    return jsonify(data)


def _add_data(data, query: BaseQuery, type_: Union[CraftingType, List[CraftingType]], level: int, num_levels: int,
              key: str = None):
    recipes_query = _crafting_type_query(query, type_)

    recipes = recipes_query.filter(Recipe.level.in_(range(level, level + num_levels))).all()
    previous = recipes_query.filter(Recipe.level < level).order_by(Recipe.level.desc()).all()
    next_ = recipes_query.filter(Recipe.level > (level + num_levels - 1)).order_by(Recipe.level.asc()).all()

    previous_level = previous[0].level if previous else None
    next_level = next_[0].level if next_ else None

    if recipes or previous or next_:
        if key is None:
            key = type_[0].value if isinstance(type_, List) else type_.value
        data[key] = {
            'recipes': [RecipeSchema().dump(recipe) for recipe in recipes],
            'previous': [RecipeSchema().dump(recipe) for recipe in previous if recipe.level == previous_level],
            'next': [RecipeSchema().dump(recipe) for recipe in next_ if recipe.level == next_level]
        }


def _crafting_type_query(query: BaseQuery, type_: Union[CraftingType, List[CraftingType]]):
    if isinstance(type_, CraftingType):
        type_ = [type_]

    types = []
    for current_type in type_:
        types.append(Type.query.filter_by(name=current_type.value,
                                          category=Category.query.filter_by(
                                              name=CategoryEnum.CRAFTING_TYPE.value).first()).first())

    return query.filter(
        Recipe.type_id.in_([current_type.id for current_type in types]))
