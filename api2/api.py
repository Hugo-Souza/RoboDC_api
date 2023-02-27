from flask import Flask, request, jsonify
from subprocess import call

app = Flask(__name__)

@app.route('/run_program', methods=['POST'])
def run_program():
    call('python ./missions/send_goal_LE1.py', shell=True)
    


if __name__ == '__main__':
    app.run()
