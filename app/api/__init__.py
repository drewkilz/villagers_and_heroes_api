from flask import Blueprint

api = Blueprint('api', __name__)

# Imported here to avoid circular dependencies
from app.api import items, recipes
