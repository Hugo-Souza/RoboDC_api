from flask import request
from flask_restx import Namespace, Resource, fields

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

api = Namespace("ros", description="ROS controller")

class ROS(Resource):
    def get(self, location):
        result = movebase_client(location)
        rospy.sleep(10)
        result = movebase_client("home")

        if result:
            return { "result": f"Deu certo! { str(result) }" }, 200
        else:
            return { "error": "Erro" }, 400

api.add_resource(ROS, "/goTo/<location>")

def movebase_client(local):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    if local == "LE-1":
        goal.target_pose.pose.position.x = -37.99 
        goal.target_pose.pose.position.y = -5.45
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "LE-2":
        goal.target_pose.pose.position.x = -30.15
        goal.target_pose.pose.position.y = -5.03
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "LE-3":
        goal.target_pose.pose.position.x = -22.68
        goal.target_pose.pose.position.y = -4.45
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "LE-4":
        goal.target_pose.pose.position.x = -15.36
        goal.target_pose.pose.position.y = -4.11
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Suporte":
        goal.target_pose.pose.position.x = -11.30
        goal.target_pose.pose.position.y = -3.92
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "PPG-CC4":
        goal.target_pose.pose.position.x = -2.54
        goal.target_pose.pose.position.y = -3.12
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Maker":
        goal.target_pose.pose.position.x = 7.46
        goal.target_pose.pose.position.y = -2.39
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "LE-5":
        goal.target_pose.pose.position.x = 9.75
        goal.target_pose.pose.position.y = -2.36
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Auditorio":
        goal.target_pose.pose.position.x = 15.37
        goal.target_pose.pose.position.y = -1.86
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Banheiros":
        goal.target_pose.pose.position.x = -38.74
        goal.target_pose.pose.position.y = -10.59
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Copa":
        goal.target_pose.pose.position.x = -38.43
        goal.target_pose.pose.position.y = -16.47
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Lig":
        goal.target_pose.pose.position.x = -38.01
        goal.target_pose.pose.position.y = -22.61
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Reunioes":
        goal.target_pose.pose.position.x = -15.52
        goal.target_pose.pose.position.y = -23.80
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Chefia":
        goal.target_pose.pose.position.x = -12.49
        goal.target_pose.pose.position.y = -23.54
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Graduacao":
        goal.target_pose.pose.position.x = -18.67
        goal.target_pose.pose.position.y = -24.17
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    elif local == "Recepcao":
        goal.target_pose.pose.position.x = -12.49
        goal.target_pose.pose.position.y = -23.54
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0
    else: #home
        goal.target_pose.pose.position.x = -1.65
        goal.target_pose.pose.position.y = -21.18
        goal.target_pose.pose.orientation.z = 1.0 
        goal.target_pose.pose.orientation.w = 0.0

    client.send_goal(goal)

    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()
