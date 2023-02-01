import os
from flask_migrate import Migrate
from src import create_app, db
from src.controller import api_bp

# Initializes app with factory method from src/__init__.py
app = create_app(os.getenv('CONFIG') or 'dev')

# API Blueprint
app.register_blueprint(api_bp)

# Database migrations
migrate = Migrate()
migrate.init_app(app, db)

if __name__ == '__main__':
    app.run()
