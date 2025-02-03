import urllib

from eppr.utils import (
    get_basic_params,
    construct_data_response,
)
from eppr.constants import DATA_OPTIONS

from eppr.data.data import get_data


def route(event, query_params):
    """

    :param event:
    :param query_params:
    """
    (
        counties,
        agents,
        property_types,
        min_year,
        max_year,
        min_beds,
        max_beds,
        min_price,
        max_price,
        min_lat,
        max_lat,
        min_lng,
        max_lng,
    ) = get_basic_params(query_params)

    page_size = int(query_params.get("pageSize", 100))
    if page_size > 10000:
        return construct_data_response(
            {"message": f"pageSize must be less than or equal to 10000"}, 400
        )

    marker = query_params.get("marker")

    data_option = query_params.get("dataOption")
    if data_option not in DATA_OPTIONS:
        return construct_data_response(
            {"message": f"invalid dataOption. Must be one of {DATA_OPTIONS}"}, 400
        )

    if event["path"] == "api/data/":
        data = get_data(
            counties,
            agents,
            property_types,
            min_year,
            max_year,
            min_beds,
            max_beds,
            min_price,
            max_price,
            data_option,
            marker,
            page_size,
        )

        if data:
            path = event.get("path", "")
            query_params = event.get("queryStringParameters", {})
            query_params["marker"] = max([d["_id"] for d in data])
            updated_query_string = urllib.parse.urlencode(query_params)
            host = event["headers"].get("Host", "localhost")
            protocol = (
                "https"
                if event["headers"].get("X-Forwarded-Proto") == "https"
                else "http"
            )
            next_url = f"{protocol}://{host}/{path}/?{updated_query_string}"

            return construct_data_response({"next": next_url, "data": data})

        return construct_data_response({"data": data})

    return construct_data_response({"message": "Path not found"}, status=404)
