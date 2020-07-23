"""Contains a methodology for preloading data related to Villagers and Heroes into the data source."""

from csv import DictReader
import os
from time import perf_counter
from typing import Type as Type_

from dacite.exceptions import MissingValueError
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from app import create_app, sql_alchemy
from app.data.item import Item
from app.data.object import Object
from app.data.recipe import Recipe
from app.models.category import Category
from app.models.character import Character  # included for auto-creation in db
from app.models.enum import ItemType, CraftingType, Class, Rarity, CategoryEnum, SkillType, Skill, \
    SubClass, Server, VillageRank, VillageProject
from app.models.item import Item as ModelItem
from app.models.load import LoadMixin
from app.models.recipe import Recipe as ModelRecipe
from app.models.roster import Roster  # included for auto-creation in db
from app.models.type import Type
from app.models.village import Village  # included for auto-creation in db
from configuration import ENV_FLASK_CONFIGURATION, DEVELOPMENT_KEY


class Data:
    @staticmethod
    def __load_data(file_path: str, data_class: Type_[Object], model_class: Type_[LoadMixin], name: str):
        with open(file_path, encoding='utf-8-sig') as file:
            reader = DictReader(file)
            total_count = 0
            for _ in reader:
                total_count += 1
            file.seek(0)
            print('Loading {} {}...'.format(total_count, name))

            count = 0
            reader = DictReader(file)
            for row in reader:
                try:
                    data_object = data_class.from_dict(row)
                except (MissingValueError, ValueError) as e:
                    raise ValueError('Failed to retrieve data from file: "{}", line: {}, row: {}. Error: {}'.format(
                        file_path, reader.line_num, row, e))

                try:
                    model_class.load(data_object)
                except IntegrityError as e:
                    raise ValueError('Failed to load data from file: "{}", line: {}, data_object: {}. Error: {}'.format(
                        file_path, reader.line_num, data_object, e))
                count += 1

                print('Loaded {} of {} {}: {}'.format(count, total_count, name, data_object.name))

            print('Loaded {} {}.'.format(count, name))

    @staticmethod
    def __load_categories_and_types(sql_alchemy_: SQLAlchemy):
        categories = [
            (CategoryEnum.CLASS, Class),
            (CategoryEnum.CRAFTING_TYPE, CraftingType),
            (CategoryEnum.ITEM_TYPE, ItemType),
            (CategoryEnum.RARITY, Rarity),
            (CategoryEnum.SKILL_TYPE, SkillType),
            (CategoryEnum.SKILL, Skill),
            (CategoryEnum.SUB_CLASS, SubClass),
            (CategoryEnum.SERVER, Server),
            (CategoryEnum.VILLAGE_RANK, VillageRank),
            (CategoryEnum.VILLAGE_PROJECT, VillageProject)
        ]

        print('Loading types in {} categories...'.format(len(categories)))

        for category, values in categories:
            category_ = Category(name=category.value)
            sql_alchemy_.session.add(category_)

            for value in values:
                type_ = Type(name=value.value, category=category_)
                sql_alchemy_.session.add(type_)

            print('Loaded category: {} with {} types.'.format(category.value, len(values)))

    @staticmethod
    def create_database(app: Flask, sql_alchemy_: SQLAlchemy):
        with app.app_context():
            engine = sql_alchemy_.get_engine(app=app)

            print('Creating {} database...'.format(engine.name))

            sql_alchemy.drop_all()
            sql_alchemy.create_all()

            print('Loading data...')

            start = perf_counter()

            Data.__load_categories_and_types(sql_alchemy_)

            Data.__load_data(r'app/data/items.csv', Item, ModelItem, 'items')

            Data.__load_data(r'app/data/recipes.csv', Recipe, ModelRecipe, 'recipes')
            
            sql_alchemy.session.commit()

            stop = perf_counter()

            print('Data loaded in {} seconds.'.format(stop - start))


def create_database():
    """
    Sets up the database and loads it with initial data.
    """

    flask_configuration = os.getenv(ENV_FLASK_CONFIGURATION)

    print('{} = {}'.format(ENV_FLASK_CONFIGURATION, flask_configuration))

    app = create_app(flask_configuration or DEVELOPMENT_KEY)

    Data.create_database(app, sql_alchemy)


if __name__ == '__main__':
    create_database()
