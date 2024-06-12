from flask import Blueprint

blueprint = Blueprint('allUsers_blueprint', __name__, url_prefix='/allUsers')

from . import routes
