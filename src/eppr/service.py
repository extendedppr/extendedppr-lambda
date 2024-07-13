import re

from eppr.constants import RESPONSE_HEADERS
from eppr.settings import (
    LISTING_PPR_DATA_OPTION,
    PPR_DATA_OPTION,
    SHARE_DATA_OPTION,
    RENTAL_DATA_OPTION,
)
from eppr.utils import (
    convert_to_json,
    construct_data_response,
)
from eppr.mongo.utils import (
    get_single_detail,
)

from eppr.map.routing import route as map_route
from eppr.chart.routing import route as chart_route


DETAIL_PATTERN = re.compile(r"api/(rental|share|listing|property)/detail")


def handler(event: dict, context):
    """

    :param event:
    :param context:
    :return:
    """
    query_params = event.get("queryStringParameters", {})

    print(event)
    print(vars(context))

    if DETAIL_PATTERN.match(event["path"]):
        obj_id = query_params.get("objId")
        data_option = event["path"].split("/")[1]
        path_to_option = {
            "rental": RENTAL_DATA_OPTION,
            "share": SHARE_DATA_OPTION,
            "listing": LISTING_PPR_DATA_OPTION,
            "property": PPR_DATA_OPTION,
        }
        collection = path_to_option.get(data_option)
        data = get_single_detail(collection, obj_id) if collection and obj_id else None

        if not data:
            return {
                "statusCode": 404,
                "headers": RESPONSE_HEADERS,
                "body": "Does not exist",
            }
        return construct_data_response({k: convert_to_json(v) for k, v in data.items()})

    if event["path"].startswith("api/map/"):
        return map_route(event, query_params)

    if event["path"].startswith("api/chart/"):
        return chart_route(event, query_params)

    return construct_data_response({"message": "Path not found"}, status=404)
