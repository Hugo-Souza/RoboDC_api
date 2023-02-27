from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run_program', methods=['POST'])
def run_program():
    program = request.files.get('program')
    if program:
        program.save(program.filename)
        try:
            output = subprocess.check_output(['python', program.filename], stderr=subprocess.STDOUT, timeout=30)
            result = {'status': 'success', 'output': output.decode('utf-8')}
        except subprocess.CalledProcessError as e:
            result = {'status': 'error', 'message': e.output.decode('utf-8')}
        except Exception as e:
            result = {'status': 'error', 'message': str(e)}
        finally:
            os.remove(program.filename)
    else:
        result = {'status': 'error', 'message': 'No program provided'}
    return jsonify(result)

if __name__ == '__main__':
    app.run()
