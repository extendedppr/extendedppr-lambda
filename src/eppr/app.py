from apiflask import APIFlask
from flask import jsonify, make_response

from eppr.api import query


def create_app():
    flask_app = APIFlask(__name__, title="EPPR", docs_ui="redoc")
    flask_app.config["SPEC_FORMAT"] = "json"
    return flask_app


app = create_app()


@app.errorhandler(Exception)
def handle_exception(ex):
    print(ex)
    return make_response(
        jsonify(
            f"Internal server error {ex}",
        ),
        500,
    )


app.register_blueprint(query.bp)
