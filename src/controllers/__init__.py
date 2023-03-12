from flask import Blueprint
from flask_restx import Api

from src.controllers.ros_controller import api as ros_ns
from src.controllers.metadata_controller import api as metadata_ns

from ..config import version

api_bp = Blueprint('api', __name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    api_bp,
    title='RoboDC API',
    version=version,
    description='API para fornecer os dados utilizados pelo RoboDC',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(ros_ns)
api.add_namespace(metadata_ns)