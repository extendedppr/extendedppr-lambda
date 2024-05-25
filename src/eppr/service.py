from eppr.constants import RESPONSE_HEADERS
from eppr.utils import (
    convert_to_json,
    construct_data_response,
)
from eppr.mongo.utils import (
    get_single_listing,
    get_single_ppr,
)

from eppr.map.routing import route as map_route
from eppr.chart.routing import route as chart_route


def handler(event, context):
    """

    :param event:
    :param context:
    :return:
    """
    query_params = event.get("queryStringParameters", {})

    print(event)
    print(vars(context))

    if event["path"] == "api/listing/detail":
        data = get_single_listing(query_params.get("objId"))
        if not data:
            return {
                "statusCode": 404,
                "headers": RESPONSE_HEADERS,
                "body": "Specified listing does not exist",
            }
        return construct_data_response({k: convert_to_json(v) for k, v in data.items()})

    if event["path"] == "api/property/detail":
        data = get_single_ppr(query_params.get("objId"))
        if not data:
            return {
                "statusCode": 404,
                "headers": RESPONSE_HEADERS,
                "body": "Specified property does not exist",
            }
        return construct_data_response({k: convert_to_json(v) for k, v in data.items()})

    if event["path"].startswith("api/map/"):
        return map_route(event, query_params)

    if event["path"].startswith("api/chart/"):
        return chart_route(event, query_params)

    return construct_data_response({"message": "Path not found"}, status=404)
