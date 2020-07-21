from flask import Blueprint, Flask, jsonify
from flask_cors import CORS


class ApiBlueprint(Blueprint):
    def init_api(self, app: Flask):
        CORS(self)


api = ApiBlueprint('api', __name__)


# Imported here to avoid circular dependencies
from app.api import authentication, items, recipes, categories, roster
