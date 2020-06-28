from http import HTTPStatus

from flask import jsonify

from app.api import api


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = HTTPStatus.FORBIDDEN
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = HTTPStatus.UNAUTHORIZED
    return response


@api.app_errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(e):
    response = jsonify({'error': 'not found', 'description': e.description})
    response.status_code = HTTPStatus.NOT_FOUND
    return response
