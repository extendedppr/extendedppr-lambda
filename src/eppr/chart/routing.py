from eppr.utils import (
    get_basic_params,
    construct_data_response,
)

from eppr.chart.data import (
    get_undervalued_by_eircode,
    get_avg_prices_by_eircode,
    get_avg_prices,
)


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
        _,
        _,
        _,
        _,
    ) = get_basic_params(query_params)

    if event["path"] == "api/chart/undervalued_by_eircode":
        avg_prices = get_undervalued_by_eircode(
            counties,
            agents,
            property_types,
            min_year,
            max_year,
            min_beds,
            max_beds,
            data_option=query_params.get("dataOption"),
        )

        return construct_data_response(avg_prices)

    if event["path"] == "api/chart/avgpricesbyeircode":
        avg_prices = get_avg_prices_by_eircode(
            counties,
            agents,
            property_types,
            min_year,
            max_year,
            min_beds,
            max_beds,
            data_option=query_params.get("dataOption"),
        )

        return construct_data_response(avg_prices)

    if event["path"] == "api/chart/avgprices":
        avg_prices = get_avg_prices(
            counties,
            agents,
            property_types,
            min_year,
            max_year,
            min_beds,
            max_beds,
            data_option=query_params.get("dataOption"),
        )

        return construct_data_response(avg_prices)

    return construct_data_response({"message": "Path not found"}, status=404)
