from eppr.mongo.utils import (
    get_time_property,
    get_price_property,
    get_collection_name,
    aggregate,
    update_match,
)
from eppr.utils import (
    is_default_beds,
)
from eppr.mongo.filters import (
    get_bed_filter,
    get_county_filter,
    get_property_type_filter,
    get_agent_filter,
    get_time_range_filter,
)


def get_undervalued_by_eircode(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    data_option: str,
) -> list:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param data_option:
    """

    pipeline = [
        {
            "$match": {
                "price": {"$exists": True, "$ne": None, "$gte": 0},
                "ppr_price": {"$exists": True, "$ne": None, "$gte": 0},
            }
        },
        {
            "$group": {
                "_id": "$eircode_routing_key",
                "count": {"$sum": 1},
                "undervalued_percent": {"$avg": "$undervalued_by_percent"},
            }
        },
    ]

    for filter_obj in [
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter(get_time_property(data_option), min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    pipeline.extend(
        [
            {
                "$project": {
                    "count": 1,
                    "undervalued_percent": {"$multiply": ["$undervalued_percent", 100]},
                }
            },
            {"$sort": {"undervalued_percent": -1}},
        ]
    )

    data = list(aggregate(get_collection_name(data_option), pipeline))

    return sorted(data, key=lambda x: x["undervalued_percent"], reverse=True)


def get_avg_prices_by_eircode(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    data_option: str,
) -> list:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param data_option:
    """

    pipeline = [
        {"$match": {}},
        {
            "$group": {
                "_id": "$eircode_routing_key",
                "averagePrice": {"$avg": f"${get_price_property(data_option)}"},
                "count": {"$sum": 1},
            }
        },
    ]

    for filter_obj in [
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter(get_time_property(data_option), min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    data = list(aggregate(get_collection_name(data_option), pipeline))

    return sorted(data, key=lambda x: x["averagePrice"], reverse=True)


def get_avg_prices(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    data_option: str,
) -> list:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param data_option:
    """

    pipeline = [
        {"$match": {}},
        {
            "$addFields": {
                "monthStartDate": {
                    "$dateFromParts": {
                        "year": {"$year": f"${get_time_property(data_option)}"},
                        "month": {"$month": f"${get_time_property(data_option)}"},
                        "day": 1,
                    }
                }
            }
        },
        {
            "$group": {
                "_id": "$monthStartDate",
                "averagePrice": {"$avg": f"${get_price_property(data_option)}"},
                "count": {"$sum": 1},
            }
        },
        {"$sort": {"_id": 1}},
        {
            "$project": {
                "monthStartDate": "$_id",
                "averagePrice": 1,
                "count": 1,
                "_id": 0,
            }
        },
    ]

    for filter_obj in [
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter(get_time_property(data_option), min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    return list(aggregate(get_collection_name(data_option), pipeline))
