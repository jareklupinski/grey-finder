from flask import Blueprint

bp = Blueprint('main', __name__, static_folder='/static', static_url_path='/static')

from app.main import routes
