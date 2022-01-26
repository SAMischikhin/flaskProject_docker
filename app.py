from typing import Tuple, Any

from flask import Flask, request
from marshmallow import ValidationError
from utils import *

app = Flask(__name__)


@app.route("/perform_query")
def perform_query() -> Tuple[Any, int]:
    try:
        data = UserSchema().load(request.args)
        content = get_content(data)
        return app.response_class(content, content_type="text/plain")
    except ValidationError as e:
        return e.normalized_messages(), 400


if __name__ == '__main__':
    app.run()
