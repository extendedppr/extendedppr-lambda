import datetime
import math
import json

from bson import ObjectId

from eppr.constants import RESPONSE_HEADERS


def convert_to_json(obj):
    """

    :param obj:
    :return:
    """
    if isinstance(obj, ObjectId):
        return str(obj)
    if isinstance(obj, float) and math.isnan(obj):
        return None
    if isinstance(obj, datetime.datetime):
        return str(obj)
    if isinstance(obj, (str, float, int, dict, list, type(None))):
        return obj
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def get_list(item):
    if isinstance(item, list):
        return item
    if isinstance(item, str):
        try:
            return json.loads(item)
        except:
            return item.split(",")


def get_basic_params(query_params: dict) -> tuple:
    """

    :param query_params:
    :return:
    """
    return (
        get_list(query_params.get("filterCounties")),
        get_list(query_params.get("filterAgents")),
        get_list(query_params.get("filterPropertyTypes")),
        query_params.get("minDate"),
        query_params.get("maxDate"),
        int(query_params.get("minBeds", 0)),
        int(query_params.get("maxBeds", 100)),
        int(query_params.get("minPrice", 0)),
        int(query_params.get("maxPrice", 100000000)),
        float(query_params.get("minLat", 0)),
        float(query_params.get("maxLat", 0)),
        float(query_params.get("minLng", 0)),
        float(query_params.get("maxLng", 0)),
    )


def construct_data_response(data: dict | list, status: int = 200) -> dict:
    """

    :param data:
    :kwargs status:
    :return:
    """
    return {
        "statusCode": status,
        "headers": RESPONSE_HEADERS,
        "body": json.dumps(
            data,
            default=convert_to_json,
        ),
    }


def is_default_beds(min_beds: int, max_beds: int) -> bool:
    """

    :param min_beds:
    :param max_beds:
    :return:
    """
    return min_beds == 0 and max_beds == 100
