import os

DEVELOPMENT_KEY = 'development'
TESTING_KEY = 'testing'
PRODUCTION_KEY = 'production'

ENV_FLASK_CONFIGURATION = 'FLASK_CONFIGURATION'
ENV_SECRET_KEY = 'SECRET_KEY'


class Configuration:
    SECRET_KEY: str = os.environ.get(ENV_SECRET_KEY)

    def init_app(self, app):
        if not self.SECRET_KEY:
            raise EnvironmentError('No {} configured in environment variables for Flask-WTF'.format(ENV_SECRET_KEY))


class DevelopmentConfiguration(Configuration):
    DEBUG: bool = True


class TestingConfiguration(Configuration):
    TESTING: bool = True


class ProductionConfiguration(Configuration):
    pass


CONFIGURATION = {
    DEVELOPMENT_KEY: DevelopmentConfiguration,
    TESTING_KEY: TestingConfiguration,
    PRODUCTION_KEY: ProductionConfiguration
}
