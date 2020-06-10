from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from configuration import CONFIGURATION

bootstrap = Bootstrap()
sql_alchemy = SQLAlchemy()


def create_app(config_name: str):
    app = Flask(__name__)
    configuration = CONFIGURATION[config_name]()
    configuration.init_app(app)
    app.config.from_object(configuration)

    bootstrap.init_app(app)
    sql_alchemy.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
