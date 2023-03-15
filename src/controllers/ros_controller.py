from flask import request
from flask_restx import Namespace, Resource, fields

import time

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

api = Namespace("ros", description="ROS controller")

goalResponseDto = api.model('goalResponseDto', {
    'available_locals': fields.List(fields.String),
})

goToResponseDto = api.model('goToResponseDto', {
    'result': fields.String,
})

stateResponseDto = api.model('stateResponseDto', {
    'goal_state': fields.String,
    'comm_state': fields.String,
})

cancelResponseDto = api.model('cancelResponseDto', {
    'result': fields.String("Mensagem de cancelamento enviada"),
})

errorResponseDto = api.model('errorResponseDto', {
    'error': fields.String,
})

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

ros_states = {
    0: "PENDING",
    1: "ACTIVE",
    2: "PREEMPTED",
    3: "SUCCEEDED",
    4: "ABORTED",
    5: "REJECTED",
    6: "PREEMPTING",
    7: "RECALLING",
    8: "RECALLED",
    9: "LOST",
}

ros_comm_state = {
    0: "WAITING_FOR_GOAL_ACK",
    1: "PENDING",
    2: "ACTIVE",
    3: "WAITING_FOR_RESULT",
    4: "WAITING_FOR_CANCEL_ACK",
    5: "RECALLING",
    6: "PREEMPTING",
    7: "DONE",
    8: "LOST"
}

# global actionlib client
client = None

class goal(Resource):
    @api.response(200, 'goalResponseDto', goalResponseDto)
    @api.response(400, 'errorResponseDto', errorResponseDto)
    def get(self):
        """Retorna a lista de todos os destinos possíveis do robô."""

        locals_list = list(available_locals.keys())
            
        return { "available_locals": locals_list }, 200

class ROS(Resource):
    @api.response(200, 'goToResponseDto', goToResponseDto)
    @api.response(400, 'errorResponseDto', errorResponseDto)
    def get(self, location):
        """Faz o robô se movimentar até o local recebido.
        Se o local recebido não estiver cadastrado, o robô se movimenta até o saguão do DC."""

        result = movebase_client(location)

        if result != None or result != 9:
            return { "result": ros_states[result] }, 200
        else:
            return { "error": str(result) }, 400

class state(Resource):
    @api.response(200, 'stateResponseDto', stateResponseDto)
    @api.response(400, 'errorResponseDto', errorResponseDto)
    def get(self):
        """Retorna o status atual do robô."""

        result = get_state_client()

        if result:
            return { 
                "goal_state": ros_states[result[0]],
                "comm_state": ros_comm_state[result[1]]
            }, 200
        else:
            return { "error": "Goal não encontrada." }, 400

class cancel(Resource):
    @api.response(200, 'cancelResponseDto', cancelResponseDto)
    @api.response(400, 'errorResponseDto', errorResponseDto)
    def delete(self):
        """Envia um request de cancelamento para todas as goals."""
        lclient = actionlib.SimpleActionClient('move_base', MoveBaseAction)

        if lclient:
            lclient.cancel_all_goals()

            return { "result": "Mensagem de cancelamento enviada." }, 200
        else:
            return { "error": "Nenhuma goal encontrada." }, 400

api.add_resource(goal, "/goal")
api.add_resource(ROS, "/goTo/<location>")
api.add_resource(state, "/status")
api.add_resource(cancel, "/cancel")

def movebase_client(local):

    global client
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)

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

    time.sleep(3)

    print(client.get_goal_status_text())
    print(client.get_state())

    return client.get_state()
        
def get_state_client():
    if client:
        return (client.get_state(), client.gh.get_comm_state())
    else:
        return None
