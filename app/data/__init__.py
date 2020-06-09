"""Contains a methodology for preloading data related to Villagers and Heroes into the data source."""

from csv import DictReader
from time import perf_counter
from typing import Type as Type_

from dacite.exceptions import MissingValueError
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.data.item import Item
from app.data.object import Object
from app.data.recipe import Recipe
from app.models.item import Item as ModelItem
from app.models.load import LoadMixin
from app.models.recipe import Recipe as ModelRecipe
from app.models.type import ItemType, CraftingType, Class, Rarity, Type, CategoryEnum, Category, SkillType, Skill, \
    SubClass
from configuration import ENV_RELOAD_DATA


class Data:
    @staticmethod
    def __load_data(file_path: str, data_class: Type_[Object], model_class: Type_[LoadMixin]):
        with open(file_path, encoding='utf-8-sig') as file:
            reader = DictReader(file)
            for line_number, row in enumerate(reader):
                try:
                    data_object = data_class.from_dict(row)
                except (MissingValueError, ValueError) as e:
                    raise ValueError('Failed to retrieve data from file: "{}", line: {}. Error: {}'.format(
                        file_path, line_number + 1, e))

                model_class.load(data_object)

    @staticmethod
    def __load_categories_and_types(sql_alchemy: SQLAlchemy):
        for category, values in [
            (CategoryEnum.CLASS, Class),
            (CategoryEnum.CRAFTING_TYPE, CraftingType),
            (CategoryEnum.ITEM_TYPE, ItemType),
            (CategoryEnum.RARITY, Rarity),
            (CategoryEnum.SKILL_TYPE, SkillType),
            (CategoryEnum.SKILL, Skill),
            (CategoryEnum.SUB_CLASS, SubClass),
        ]:
            category_ = Category(name=category.value)
            sql_alchemy.session.add(category_)

            for value in values:
                type_ = Type(name=value.value, category=category_)
                sql_alchemy.session.add(type_)

    def init_app(self, app: Flask, sql_alchemy: SQLAlchemy):
        if not app.config[ENV_RELOAD_DATA]:
            return

        print('Loading data...')

        with app.app_context():
            start = perf_counter()

            # Cannot use sql_alchemy.drop_all() as it was throwing sqlalchemy.exc.ProgrammingError:
            #  (psycopg2.errors.UndefinedTable) table "xxx" does not exist, while connected to the production PostgreSQL
            #  instance
            engine = sql_alchemy.get_engine(app=app)
            for table in sql_alchemy.get_tables_for_bind():
                if table.exists(bind=engine):
                    table.drop(bind=engine)

            sql_alchemy.create_all()

            print('Loading types and categories...')
            self.__load_categories_and_types(sql_alchemy)

            print('Loading items...')
            self.__load_data(r'app/data/items.csv', Item, ModelItem)

            print('Loading recipes...')
            self.__load_data(r'app/data/recipes.csv', Recipe, ModelRecipe)

            sql_alchemy.session.commit()

            stop = perf_counter()

            print('Data loaded in {} seconds.'.format(stop - start))
