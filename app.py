import os

from flask import Flask, request, Response
from .helpers import get_response
from typing import Tuple, Union

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=('POST',))
def perform_query() -> Union[Tuple[str, int], Response]:
    params = request.form.to_dict()
    if len({'value1', 'value2', 'cmd1', 'cmd2', 'file_name'} & set(params.keys())) != 5:
        return 'Args validation error', 400
    try:
        ret = get_response(params)
        return app.response_class(ret, content_type='text/plain')
    except Exception as e:
        print(e)
        return 'Some exception occurred T_T', 500
