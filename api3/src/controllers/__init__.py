from flask import Blueprint
from flask_restx import Api

from src.controllers.hello_controller import api as hello_ns
from src.controllers.ros_controller import api as ros_ns
from src.controllers.metadata_controller import api as metadata_ns

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
    version='1.0',
    description='API para fornecer os dados utilizados pelo RoboDC',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(hello_ns)
api.add_namespace(ros_ns)
api.add_namespace(metadata_ns)