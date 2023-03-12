from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from .config import config_by_name
from flask.app import Flask

db = SQLAlchemy()
flask_bcrypt = Bcrypt()

def create_app(config_name: str) -> Flask:
    app = Flask(__name__)

    CORS(app, resources={"*": {"origins": "*"}})

    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    flask_bcrypt.init_app(app)

    return app