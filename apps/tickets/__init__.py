from flask import Blueprint

blueprint = Blueprint('tickets_blueprint', __name__, url_prefix='/tickets')

# Import routes to register them with the blueprint
from . import routes
