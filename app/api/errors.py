from http import HTTPStatus

from flask import jsonify, request

from app.api import api


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = HTTPStatus.FORBIDDEN
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = HTTPStatus.UNAUTHORIZED
    return response


@api.app_errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found', 'description': e.description})
    response.status_code = 404
    return response
