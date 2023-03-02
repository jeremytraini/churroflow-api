import signal
from json import dumps
from flask import Flask, request, send_from_directory
from flask_cors import CORS # type: ignore
from src import config
from src.health_check import health_check_v1

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__, static_url_path='/static/')
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

@APP.route("/health_check/v1", methods=['GET'])
def health_check():
    
    return dumps(health_check_v1())


# Samples below

@APP.route("/test/post/v1", methods=['POST'])
def test_post():
    data = request.json
    val = data["val"]
    
    return dumps(val)

@APP.route("/test/get/v1", methods=['GET'])
def test_get():
    val = request.args.get('val')
    
    return dumps(val)

@APP.route("/test/put/v1", methods=['PUT'])
def test_put(): 
    data = request.json
    val = data['val']

    return dumps(val)

@APP.route("/test/delete/v1", methods=['DELETE'])
def test_delete(): 
    data = request.json
    val = data['val']

    return dumps(val)

#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
