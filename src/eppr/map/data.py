import math
import copy

from eppr.settings import (
    LISTING_PPR_DATA_OPTION,
    MATCHED_WITH_PPR_DATA_OPTION,
    SHARE_DATA_OPTION,
    RENTAL_DATA_OPTION,
)
from eppr.constants import SAMPLE_SIZE, EMPTY_GEOJSON
from eppr.mongo.utils import (
    get_poly,
    aggregate,
    update_match,
)
from eppr.mongo.filters import (
    get_price_filter,
    get_bed_filter,
    get_county_filter,
    get_property_type_filter,
    get_agent_filter,
    get_time_range_filter,
)


def get_listings(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    min_price: int,
    max_price: int,
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
) -> dict:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param min_price:
    :param max_price:
    :param min_latitude:
    :param max_latitude:
    :param min_longitude:
    :param max_longitude:
    """

    pipeline = [
        {
            "$match": {
                "location": {
                    "$geoWithin": {
                        "$geometry": get_poly(
                            min_latitude, max_latitude, min_longitude, max_longitude
                        )
                    }
                }
            }
        },
        {"$sample": {"size": SAMPLE_SIZE}},
        {
            "$project": {
                "price": "$price",
                "coords": {
                    "$map": {
                        "input": "$location.coordinates",
                        "as": "coord",
                        "in": {"$round": ["$$coord", 6]},
                    }
                },
            }
        },
    ]

    for filter_obj in [
        get_price_filter("price", min_price, max_price),
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter("published_date", min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    geojson = copy.deepcopy(EMPTY_GEOJSON)

    for datapoint in list(aggregate(LISTING_PPR_DATA_OPTION, pipeline)):
        if math.isnan(datapoint["coords"][0]):
            continue

        geojson["features"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": datapoint["coords"]},
                "properties": {"price": datapoint["price"], "_id": datapoint["_id"]},
            }
        )

    return geojson


def get_matching_listings_prices(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    min_price: int,
    max_price: int,
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
) -> dict:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param min_price:
    :param max_price:
    :param min_latitude:
    :param max_latitude:
    :param min_longitude:
    :param max_longitude:
    """

    pipeline = [
        {
            "$match": {
                "location": {
                    "$geoWithin": {
                        "$geometry": get_poly(
                            min_latitude, max_latitude, min_longitude, max_longitude
                        )
                    }
                },
            }
        },
        {"$sample": {"size": SAMPLE_SIZE}},
        {
            "$project": {
                "sp": "$ppr_price",
                "coords": {
                    "$map": {
                        "input": "$location.coordinates",
                        "as": "coord",
                        "in": {"$round": ["$$coord", 6]},
                    }
                },
            }
        },
    ]

    for filter_obj in [
        get_price_filter("ppr_price", min_price, max_price),
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter("ppr_sale_date", min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    geojson = copy.deepcopy(EMPTY_GEOJSON)

    for datapoint in list(aggregate(MATCHED_WITH_PPR_DATA_OPTION, pipeline)):
        if math.isnan(datapoint["coords"][0]):
            continue

        geojson["features"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": datapoint["coords"]},
                "properties": {"price": datapoint["sp"], "_id": datapoint["_id"]},
            }
        )

    return geojson


def get_matching_listings(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    min_price: int,
    max_price: int,
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
) -> dict:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param min_price:
    :param max_price:
    :param min_latitude:
    :param max_latitude:
    :param min_longitude:
    :param max_longitude:
    """

    pipeline = [
        {
            "$match": {
                "location": {
                    "$geoWithin": {
                        "$geometry": get_poly(
                            min_latitude, max_latitude, min_longitude, max_longitude
                        )
                    }
                },
            }
        },
        {"$sample": {"size": SAMPLE_SIZE}},
        {
            "$project": {
                "under_pc": "$undervalued_by_percent",
                "coords": {
                    "$map": {
                        "input": "$location.coordinates",
                        "as": "coord",
                        "in": {"$round": ["$$coord", 6]},
                    }
                },
            }
        },
    ]

    for filter_obj in [
        get_price_filter("ppr_price", min_price, max_price),
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter("ppr_sale_date", min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    geojson = copy.deepcopy(EMPTY_GEOJSON)

    for datapoint in list(aggregate(MATCHED_WITH_PPR_DATA_OPTION, pipeline)):
        if math.isnan(datapoint["coords"][0]):
            continue

        datapoint["under_pc"] = (
            None
            if math.isnan(datapoint["under_pc"])
            else float(datapoint["under_pc"]) * 100
        )

        geojson["features"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": datapoint["coords"]},
                "properties": {
                    "under_pc": datapoint["under_pc"],
                    "_id": datapoint["_id"],
                },
            }
        )

    return geojson


def get_prices(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    min_price: int,
    max_price: int,
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
) -> dict:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param min_price:
    :param max_price:
    :param min_latitude:
    :param max_latitude:
    :param min_longitude:
    :param max_longitude:
    """

    pipeline = [
        {
            "$match": {
                "location": {
                    "$geoWithin": {
                        "$geometry": get_poly(
                            min_latitude, max_latitude, min_longitude, max_longitude
                        )
                    }
                },
            }
        },
        {"$sample": {"size": SAMPLE_SIZE}},
        {
            "$project": {
                "sp": "$ppr_price",
                "coords": {
                    "$map": {
                        "input": "$location.coordinates",
                        "as": "coord",
                        "in": {"$round": ["$$coord", 6]},
                    }
                },
            }
        },
    ]

    for filter_obj in [
        get_price_filter("ppr_price", min_price, max_price),
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter("ppr_sale_date", min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    geojson = copy.deepcopy(EMPTY_GEOJSON)

    for datapoint in list(aggregate(MATCHED_WITH_PPR_DATA_OPTION, pipeline)):
        if math.isnan(datapoint["coords"][0]):
            continue

        geojson["features"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": datapoint["coords"]},
                "properties": {
                    "price": datapoint["sp"],
                    "_id": datapoint["_id"],
                },
            }
        )

    return geojson


def get_rentals(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    min_price: int,
    max_price: int,
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
) -> dict:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param min_price:
    :param max_price:
    :param min_latitude:
    :param max_latitude:
    :param min_longitude:
    :param max_longitude:
    """

    pipeline = [
        {
            "$match": {
                "location": {
                    "$geoWithin": {
                        "$geometry": get_poly(
                            min_latitude, max_latitude, min_longitude, max_longitude
                        )
                    }
                },
            }
        },
        {"$sample": {"size": SAMPLE_SIZE}},
        {
            "$project": {
                "price": "$price",
                "coords": {
                    "$map": {
                        "input": "$location.coordinates",
                        "as": "coord",
                        "in": {"$round": ["$$coord", 6]},
                    }
                },
            }
        },
    ]

    for filter_obj in [
        get_price_filter("price", min_price, max_price),
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter("published_date", min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    geojson = copy.deepcopy(EMPTY_GEOJSON)

    for datapoint in list(aggregate(RENTAL_DATA_OPTION, pipeline)):
        if math.isnan(datapoint["coords"][0]):
            continue

        geojson["features"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": datapoint["coords"]},
                "properties": {
                    "price": datapoint["price"],
                    "_id": datapoint["_id"],
                },
            }
        )

    return geojson


def get_shares(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    min_price: int,
    max_price: int,
    min_latitude: float,
    max_latitude: float,
    min_longitude: float,
    max_longitude: float,
) -> dict:
    """

    :param counties:
    :param agents:
    :param property_types:
    :param min_year:
    :param max_year:
    :param min_beds:
    :param max_beds:
    :param min_price:
    :param max_price:
    :param min_latitude:
    :param max_latitude:
    :param min_longitude:
    :param max_longitude:
    """
    pipeline = [
        {
            "$match": {
                "location": {
                    "$geoWithin": {
                        "$geometry": get_poly(
                            min_latitude, max_latitude, min_longitude, max_longitude
                        )
                    }
                },
            }
        },
        {"$sample": {"size": SAMPLE_SIZE}},
        {
            "$project": {
                "price": "$price",
                "coords": {
                    "$map": {
                        "input": "$location.coordinates",
                        "as": "coord",
                        "in": {"$round": ["$$coord", 6]},
                    }
                },
            }
        },
    ]

    for filter_obj in [
        get_price_filter("price", min_price, max_price),
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter("published_date", min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    geojson = copy.deepcopy(EMPTY_GEOJSON)

    for datapoint in list(aggregate(SHARE_DATA_OPTION, pipeline)):
        if math.isnan(datapoint["coords"][0]):
            continue

        geojson["features"].append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": datapoint["coords"]},
                "properties": {
                    "price": datapoint["price"],
                    "_id": datapoint["_id"],
                },
            }
        )

    return geojson
