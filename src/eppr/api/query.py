import uuid
import json

from apiflask import APIBlueprint
from flask import request

from eppr.api.utils import convert_response
from eppr.service import handler
from eppr.constants import RESPONSE_HEADERS

bp = APIBlueprint("query", "query")


class AWSContext:
    def __init__(self) -> None:
        self.aws_request_id = str(uuid.uuid4())


@bp.route(
    "/<path:path>",
    methods=["GET"],
)
def wild_card_route(path):
    context = AWSContext()
    event = {"path": path, "httpMethod": request.method}
    if request.is_json:
        event["body"] = dict(request.json)
    if request.args:
        event["queryStringParameters"] = dict(request.args)
    if request.headers:
        event["headers"] = dict(request.headers)

    try:
        return convert_response(handler(event, context))
    except Exception as ex:
        print(ex)

    return {
        "statusCode": 500,
        "headers": RESPONSE_HEADERS,
        "body": json.dumps({"message": "error"}),
    }
