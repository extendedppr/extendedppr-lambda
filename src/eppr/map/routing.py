from eppr.utils import (
    get_basic_params,
    construct_data_response,
)

from eppr.map.data import (
    get_listings,
    get_matching_listings,
    get_prices,
    get_rentals,
    get_shares,
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
        min_latitude,
        max_latitude,
        min_longitude,
        max_longitude,
    ) = get_basic_params(query_params)

    if event["path"] == "api/map/list/ppr_price":
        return construct_data_response(
            get_prices(
                counties,
                agents,
                property_types,
                min_year,
                max_year,
                min_beds,
                max_beds,
                min_price,
                max_price,
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude,
            )
        )

    if event["path"] == "api/map/list/undervalued":
        return construct_data_response(
            get_matching_listings(
                counties,
                agents,
                property_types,
                min_year,
                max_year,
                min_beds,
                max_beds,
                min_price,
                max_price,
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude,
            )
        )

    if event["path"] == "api/map/list/listings":
        return construct_data_response(
            get_listings(
                counties,
                agents,
                property_types,
                min_year,
                max_year,
                min_beds,
                max_beds,
                min_price,
                max_price,
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude,
            )
        )

    if event["path"] == "api/map/list/rentals":
        return construct_data_response(
            get_rentals(
                counties,
                agents,
                property_types,
                min_year,
                max_year,
                min_beds,
                max_beds,
                min_price,
                max_price,
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude,
            )
        )

    if event["path"] == "api/map/list/shares":
        return construct_data_response(
            get_shares(
                counties,
                agents,
                property_types,
                min_year,
                max_year,
                min_beds,
                max_beds,
                min_price,
                max_price,
                min_latitude,
                max_latitude,
                min_longitude,
                max_longitude,
            )
        )

    return construct_data_response({"message": "Path not found"}, status=404)
