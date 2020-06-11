from http import HTTPStatus

from flask import jsonify


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = HTTPStatus.FORBIDDEN
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = HTTPStatus.UNAUTHORIZED
    return response
