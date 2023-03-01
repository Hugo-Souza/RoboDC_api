import os
from flask_migrate import Migrate
from src import create_app, db
from src.controllers import api_bp

import rospy

# Initializes app with factory method from src/__init__.py
app = create_app(os.getenv('CONFIG') or 'dev')

# API Blueprint
app.register_blueprint(api_bp)

# Database migrations
migrate = Migrate()
migrate.init_app(app, db)

if __name__ == '__main__':
    rospy.init_node(os.getenv('ROS_NODE') or 'movebase_client_py',anonymous=True)
    app.run(host="0.0.0.0",port=5000)