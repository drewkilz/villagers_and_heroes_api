import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from configuration import CONFIGURATION
from .crafting_calculator import CraftingCalculator, CraftingOptions
from .db import Data
from .models.crafting_list import CraftingList

bootstrap = Bootstrap()
data = Data()


def create_app(config_name):
    app = Flask(__name__)
    configuration = CONFIGURATION[config_name]()
    app.config.from_object(configuration)
    configuration.init_app(app)

    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
