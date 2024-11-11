from flask import request
from flask_restx import Namespace, Resource, fields

import bluetooth as bt

api = Namespace("led", description="LED controller")

esp32 = "HEAD"
address = "8C:AA:B5:93:69:EE"

expressions = {
    9: "face happy",
    17: "face sad",
    10: "eyes neutral",
    18: "eyes closed",
    26: "eyes partially_closed ",
    34: "eyes partially_open",
    42: "eyes slight_left",
    50: "eyes left",
    58: "eyes realleft",
    66: "eyes slight_right",
    74: "eyes right",
    82: "eyes real_right",
    11: "left eye neutral",
    19: "left eye closed",
    27: "left eye partially_closed",
    35: "left eye partially_open",
    43: "left eye slight_left",
    51: "left eye left",
    59: "left eye realleft",
    67: "left eye slight_right",
    75: "left eye right",
    83: "left eye real_right",
    12: "right eye neutral",
    20: "right eye closed",
    28: "right eye partially_closed",
    36: "right eye partially_open",
    44: "right eye slight_left",
    52: "right eye left",
    60: "right eye realleft",
    68: "right eye slight_right",
    76: "right eye right",
    84: "right eye real_right",
    13: "mouth happy",
    21: "mouth sad",
    29: "mouth verry_happy",
    37: "mouth partially_open",
    45: "mouth neutral",
    53: "mouth opened",
}

class changeExpression(Resource):
    def get(self, expressionNumber):
        try:
            port = 1
            socket = bt.BluetoothSocket(bt.RFCOMM)
            socket.connect((address, port)) 
            socket.send(bytes([int(expressionNumber)]))	
            socket.close()
            return { 
                "result": "OK", 
                "expressionNumber": expressionNumber,
                "expressionBits": bin(int(expressionNumber)),
            }, 200
        except Exception as e:
            return { 
                "error": "Request to change robot expression failed.",
                "message": str(e) 
            }, 400
        
    def post(self):
        try:
            data = request.get_json()
            expression_values = data.get('expressionValues', [])

            if not expression_values:
                return {"error": "A lista de expressionNumbers está vazia."}, 400

            port = 1
            socket = bt.BluetoothSocket(bt.RFCOMM)
            socket.connect((address, port))

            for expression_value in expression_values:
                socket.send(bytes([int(expression_value)]))

            socket.close()

            return {
                "result": "OK",
                "sentExpressions": expression_values
            }, 200
        except Exception as e:
            return {
                "error": "Request to change robot expression failed.",
                "message": str(e)
            }, 400
        
class changeExpressionByBits(Resource):
    def get(self, expressionBits):
        try:
            port = 1
            socket = bt.BluetoothSocket(bt.RFCOMM)
            socket.connect((address, port)) 
            socket.send(bytes([int(expressionBits, 2)]))	
            socket.close()
            return { 
                "result": "OK", 
                "expressionNumber": int(expressionBits, 2),
                "expressionBits": expressionBits,
            }, 200
        except Exception as e:
            return {
                "error": "Request to change robot expression failed.",
                "message": str(e)
            }, 400

class getExpressionsList(Resource):
    def get(self):
        try:
            return expressions, 200
        except Exception as e:
            return {
                "error": "Request to change robot expression failed.",
                "message": str(e)
            }, 400

api.add_resource(changeExpression, "/changeExpression/<expressionNumber>")
api.add_resource(changeExpression, "/changeExpression")
api.add_resource(changeExpressionByBits, "/changeExpressionByBits/<expressionBits>")
api.add_resource(getExpressionsList, "/getExpressionsList")