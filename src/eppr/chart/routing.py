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
        min_price,
        max_price,
        _,
        _,
        _,
        _,
    ) = get_basic_params(query_params)

    if event["path"] == "api/chart/undervalued_by_eircode":
        return construct_data_response(
            get_undervalued_by_eircode(
                counties,
                agents,
                property_types,
                min_year,
                max_year,
                min_beds,
                max_beds,
                min_price,
                max_price,
                data_option=query_params.get("dataOption"),
            )
        )

    if event["path"] == "api/chart/avgpricesbyeircode":
        return construct_data_response(
            get_avg_prices_by_eircode(
                counties,
                agents,
                property_types,
                min_year,
                max_year,
                min_beds,
                max_beds,
                min_price,
                max_price,
                data_option=query_params.get("dataOption"),
            )
        )

    if event["path"] == "api/chart/avgprices":
        return construct_data_response(
            get_avg_prices(
                counties,
                agents,
                property_types,
                min_year,
                max_year,
                min_beds,
                max_beds,
                min_price,
                max_price,
                data_option=query_params.get("dataOption"),
            )
        )

    return construct_data_response({"message": "Path not found"}, status=404)
