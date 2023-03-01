from flask import request
from flask_restx import Namespace, Resource, fields

from src.config import version

api = Namespace("metadata", description="API Metadata")

class Version(Resource):
    def get(self):
        return { "version": version }, 200

api.add_resource(Version, "/version")