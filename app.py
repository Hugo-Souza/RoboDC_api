import os
import threading
import rospy

from flask_migrate import Migrate
from src import create_app, db
from src.controllers import api_bp


# Initializes app with factory method from src/__init__.py
app = create_app(os.getenv('CONFIG') or 'dev')

# API Blueprint
app.register_blueprint(api_bp)

# Database migrations
migrate = Migrate()
migrate.init_app(app, db)

if __name__ == '__main__':
    threading.Thread(
        target=lambda: rospy.init_node(os.getenv('ROS_NODE') or 'movebase_client_py', anonymous=True, log_level=rospy.DEBUG, disable_signals=True)
    ).start()

    app.run(host="0.0.0.0", port=5000)