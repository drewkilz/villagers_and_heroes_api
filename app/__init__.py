from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from app.converters import StringOrIntConverter
from app.json import Encoder
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

    app.url_map.converters['str_or_int'] = StringOrIntConverter
    app.json_encoder = Encoder

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app
