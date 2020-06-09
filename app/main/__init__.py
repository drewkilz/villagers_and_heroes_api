from flask import Blueprint

main = Blueprint('main', __name__)

# Imported here to avoid circular dependencies
from app.main import views, errors
