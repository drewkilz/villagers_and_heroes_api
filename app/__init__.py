from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from configuration import CONFIGURATION

bootstrap = Bootstrap()
sql_alchemy = SQLAlchemy()

# Import here for circular dependency reasons
from app.data import Data
data = Data()


def create_app(config_name):
    app = Flask(__name__)
    configuration = CONFIGURATION[config_name]()
    configuration.init_app(app)
    app.config.from_object(configuration)

    bootstrap.init_app(app)
    sql_alchemy.init_app(app)
    data.init_app(app, sql_alchemy)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
