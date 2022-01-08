import os

from flask import Flask, request, Response
from .helpers import get_response

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=('POST',))
def perform_query() -> Response:
    params = request.form.to_dict()
    if len({'value1', 'value2', 'cmd1', 'cmd2', 'file_name'} & set(params.keys())) != 5:
        return app.response_class(
            response='Args validation error',
            status=400,
            content_type='text/plain'
        )
    try:
        return app.response_class(
            response=get_response(params),
            content_type='text/plain'
        )
    except Exception as e:
        print(e)
        return app.response_class(
            response='Some exception occurred T_T',
            status=500,
            content_type='text/plain'
        )
