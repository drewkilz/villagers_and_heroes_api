from flask import Blueprint, Flask, jsonify
from flask_cors import CORS

from configuration import ENV_CORS_ORIGIN


class ApiBlueprint(Blueprint):
    def init_api(self, app: Flask):
        cors_origin = app.config[ENV_CORS_ORIGIN]
        if cors_origin:
            # Enable CORS if specified
            CORS(self, origins=cors_origin)


api = ApiBlueprint('api', __name__)


# Imported here to avoid circular dependencies
from app.api import authentication, items, recipes, categories, roster


@api.route('/')
def get():
    return jsonify({
        'alive': True
    })
