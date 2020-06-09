from distutils.util import strtobool
import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEVELOPMENT_KEY = 'development'
TESTING_KEY = 'testing'
PRODUCTION_KEY = 'production'

ENV_FLASK_CONFIGURATION = 'FLASK_CONFIGURATION'
ENV_RELOAD_DATA = 'RELOAD_DATA'
ENV_SQLALCHEMY_DATABASE_URI = 'SQLALCHEMY_DATABASE_URI'
ENV_SQLALCHEMY_TRACK_MODIFICATIONS = 'SQLALCHEMY_TRACK_MODIFICATIONS'


class Configuration:
    RELOAD_DATA: bool = False
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(ENV_SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS: str = os.environ.get(ENV_SQLALCHEMY_TRACK_MODIFICATIONS) or False

    def init_app(self, app):
        if not self.SQLALCHEMY_DATABASE_URI:
            raise EnvironmentError('No {} configured in environment variables for Flask-SQLAlchemy'.format(
                ENV_SQLALCHEMY_DATABASE_URI))

        reload_data_string = os.environ.get(ENV_RELOAD_DATA)
        if reload_data_string:
            try:
                self.RELOAD_DATA = strtobool(reload_data_string)
            except ValueError as e:
                raise EnvironmentError('"{}" for environment variable: "{}"'.format(e, ENV_RELOAD_DATA))


class DevelopmentConfiguration(Configuration):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class TestingConfiguration(Configuration):
    TESTING: bool = True


class ProductionConfiguration(Configuration):
    pass


CONFIGURATION = {
    DEVELOPMENT_KEY: DevelopmentConfiguration,
    TESTING_KEY: TestingConfiguration,
    PRODUCTION_KEY: ProductionConfiguration
}
