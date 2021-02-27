from flask import Flask, Response
from pkg.msg import message
import json


app = Flask(__name__)


@app.route("/")
def index():
    response = {'status': False, 'message': None}
    mssg = message()
    if mssg:
        response['status'] = True
        response['message'] = mssg
    return json.dumps(response)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
