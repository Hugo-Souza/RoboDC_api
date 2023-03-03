from flask import request
from flask_restx import Namespace, Resource, fields

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

api = Namespace("ros", description="ROS controller")

available_locals = {
    "LE-1": (-37.99, -5.45, 1.0, 0.0),
    "LE-2": (-30.15, -5.03, 1.0, 0.0),
    "LE-3": (-22.68, -4.45, 1.0, 0.0),
    "LE-4": (-15.36, -4.11, 1.0, 0.0),
    "Suporte": (-11.30, -3.92, 1.0, 0.0),
    "PPG-CC4": (-2.54, -3.12, 1.0, 0.0),
    "Maker": (7.46, -2.39, 1.0, 0.0),
    "LE-5": (9.75, -2.36, 1.0, 0.0),
    "Auditorio": (15.37, -1.86, 1.0, 0.0),
    "Banheiros": (-38.74, -10.59, 1.0, 0.0),
    "Copa": (-38.43, -16.47, 1.0, 0.0),
    "Lig": (-38.01, -22.61, 1.0, 0.0),
    "Reunioes": (-15.52, -23.80, 1.0, 0.0),
    "Chefia": (-12.49, -23.54, 1.0, 0.0),
    "Graduacao": (-18.67, -24.17, 1.0, 0.0),
    "Recepcao": (-12.49, -23.54, 1.0, 0.0),
    "Home": (-1.65, -21.18, 1.0, 0.0)
}


class goal(Resource):
    def get(self):
        """Retorna a lista de todos os destinos possíveis do robô."""

        locals_list = list(available_locals.keys())
            
        return { "available_locals": locals_list }, 200


class ROS(Resource):
    def get(self, location):
        """Faz o robô se movimentar até o local recebido.
        Se o local recebido não estiver cadastrado, o robô se movimenta até o saguão do DC."""

        result = movebase_client(location)

        if result:
            return { "result": f"Deu certo! { str(result) }" }, 200
        else:
            return { "error": "Erro" }, 400


api.add_resource(goal, "/goal")
api.add_resource(ROS, "/goTo/<location>")

def movebase_client(local):

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    if local in available_locals:
        goal.target_pose.pose.position.x = available_locals[local][0]
        goal.target_pose.pose.position.y = available_locals[local][1]
        goal.target_pose.pose.orientation.z = available_locals[local][2]
        goal.target_pose.pose.orientation.w = available_locals[local][3]
    else:
        goal.target_pose.pose.position.x = available_locals["Home"][0]
        goal.target_pose.pose.position.y = available_locals["Home"][1]
        goal.target_pose.pose.orientation.z = available_locals["Home"][2]
        goal.target_pose.pose.orientation.w = available_locals["Home"][3]
  
    client.send_goal(goal)

    wait = client.wait_for_result()

    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()
        
