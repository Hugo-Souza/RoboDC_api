from flask import request
from flask_restx import Namespace, Resource, fields

from typing import Dict, Tuple

api = Namespace("hello", description="Example controller")

article_fields = api.model(
    "Article", {"title": fields.String, "content": fields.String}
)

class Hello(Resource):
    def get(self):
        return { "message": "Hello World" }, 200

api.add_resource(Hello, "")