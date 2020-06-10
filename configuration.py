import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

DEVELOPMENT_KEY = 'development'
TESTING_KEY = 'testing'
PRODUCTION_KEY = 'production'

ENV_FLASK_CONFIGURATION = 'FLASK_CONFIGURATION'
ENV_SQLALCHEMY_DATABASE_URI = 'SQLALCHEMY_DATABASE_URI'
ENV_SQLALCHEMY_TRACK_MODIFICATIONS = 'SQLALCHEMY_TRACK_MODIFICATIONS'
ENV_VNH_ITEMS_PER_PAGE = 'VNH_ITEMS_PER_PAGE'
ENV_VNH_RECIPES_PER_PAGE = 'VNH_RECIPES_PER_PAGE'


class Configuration:
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(ENV_SQLALCHEMY_DATABASE_URI) or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS: str = os.environ.get(ENV_SQLALCHEMY_TRACK_MODIFICATIONS) or False
    VNH_ITEMS_PER_PAGE = 100
    VNH_RECIPES_PER_PAGE = 100

    def init_app(self, app: Flask):
        if not self.SQLALCHEMY_DATABASE_URI:
            raise EnvironmentError('No {} configured in environment variables for Flask-SQLAlchemy'.format(
                ENV_SQLALCHEMY_DATABASE_URI))


class DevelopmentConfiguration(Configuration):
    DEBUG: bool = True


class TestingConfiguration(Configuration):
    TESTING: bool = True


class ProductionConfiguration(Configuration):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or Configuration.SQLALCHEMY_DATABASE_URI


CONFIGURATION = {
    DEVELOPMENT_KEY: DevelopmentConfiguration,
    TESTING_KEY: TestingConfiguration,
    PRODUCTION_KEY: ProductionConfiguration
}
