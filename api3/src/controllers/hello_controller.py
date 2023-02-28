from flask import request
from flask_restx import Namespace, Resource, fields

from typing import Dict, Tuple

api = Namespace("hello", description="Example controller")

class Hello(Resource):
    def get(self):
        return { "message": "Hello World" }, 200

api.add_resource(Hello, "")