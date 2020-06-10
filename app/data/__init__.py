"""Contains a methodology for preloading data related to Villagers and Heroes into the data source."""

from csv import DictReader
from threading import Lock
from time import perf_counter
from typing import Type as Type_, Any

from dacite.exceptions import MissingValueError
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import ProgrammingError, IntegrityError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DropTable

from app.data.item import Item
from app.data.object import Object
from app.data.recipe import Recipe
from app.models.item import Item as ModelItem
from app.models.load import LoadMixin
from app.models.recipe import Recipe as ModelRecipe
from app.models.type import ItemType, CraftingType, Class, Rarity, Type, CategoryEnum, Category, SkillType, Skill, \
    SubClass
from configuration import ENV_RELOAD_DATA

POSTGRESQL = 'postgresql'


@compiles(DropTable, POSTGRESQL)
def _compile_drop_table(element, compiler, **kwargs):
    """Fixes an issue with PostgreSQL, allowing drop table statements to cascade, as otherwise errors are thrown."""
    return compiler.visit_drop_table(element) + " CASCADE"


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

                # print('\rLoading {}:{} -> {}'.format(file_path, line_number + 1, data_object))
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

        with app.app_context():
            engine = sql_alchemy.get_engine(app=app)

            # Locking is required to get around PostgreSQL Integrity errors that were occurring
            #  sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) duplicate key value violates unique
            #  constraint "pg_type_typname_nsp_index"
            if engine.dialect.name == POSTGRESQL:
                lock = Lock()
                with lock:
                    self._load_data(sql_alchemy, engine)
            else:
                self._load_data(sql_alchemy, engine)

    def _load_data(self, sql_alchemy: SQLAlchemy, engine: Any):
        print('Loading data...')

        start = perf_counter()

        # Cannot use sql_alchemy.drop_all() as it was throwing sqlalchemy.exc.ProgrammingError:
        #  (psycopg2.errors.UndefinedTable) table "xxx" does not exist, while connected to the production PostgreSQL
        #  instance
        for table in sql_alchemy.get_tables_for_bind():
            try:
                if not table.exists(bind=engine):
                    table.drop(bind=engine)
            except ProgrammingError as e:
                if '(psycopg2.errors.UndefinedTable)' in str(e):
                    pass
                else:
                    raise e

        # Cannot use sql_alchemy.create_all() as it was throwing sqlalchemy.exc.IntegrityError:
        #  (psycopg2.errors.UniqueViolation) duplicate key value violates unique constraint
        #  "pg_type_typname_nsp_index", while connected to the production PostgreSQL instance
        for table in sql_alchemy.get_tables_for_bind():
            try:
                if not table.exists(bind=engine):
                    table.create(bind=engine)
            except IntegrityError as e:
                if '(psycopg2.errors.UniqueViolation)' in str(e):
                    pass
                else:
                    raise e

        print('Loading types and categories...')
        self.__load_categories_and_types(sql_alchemy)

        sql_alchemy.session.commit()

        print('Loading items...')
        self.__load_data(r'app/data/items.csv', Item, ModelItem)

        sql_alchemy.session.commit()

        print('Loading recipes...')
        self.__load_data(r'app/data/recipes.csv', Recipe, ModelRecipe)

        sql_alchemy.session.commit()

        stop = perf_counter()

        print('Data loaded in {} seconds.'.format(stop - start))
