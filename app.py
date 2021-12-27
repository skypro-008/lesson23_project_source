import os

from flask import Flask, request
from .helpers import compose_closures, get_closure

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def read_file(file_name):
    for row in open(f'data/{file_name}', 'r'):
        yield row


def get_response(params: dict):
    logs = read_file(params['file_name'])
    return compose_closures(
        get_closure(params['cmd1'], params['value1']),
        get_closure(params['cmd2'], params['value2'])
    )(logs)


@app.route("/perform_query", methods=('POST',))
def perform_query():
    params = request.form.to_dict()
    if len({'value1', 'value2', 'cmd1', 'cmd2', 'file_name'} & set(params.keys())) != 5:
        return 'Args validation error', 400
    try:
        ret = get_response(params)
        return app.response_class(ret, content_type='text/plain')
    except Exception as e:
        print(e)
        return 'Some exception occured T_T', 500
