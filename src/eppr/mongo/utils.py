from functools import cache

from pymongo.mongo_client import MongoClient
from bson import ObjectId

from eppr.settings import (
    MONGO_USER,
    MONGO_PASS,
    MONGO_HOST,
    LISTING_PPR_DATA_OPTION,
    MATCHED_WITH_PPR_DATA_OPTION,
    PPR_DATA_OPTION,
)


def aggregate(collection: str, pipeline: list):
    """

    :param collection:
    :param pipeline:
    """
    return getattr(get_client().eppr, collection).aggregate(pipeline)


def _get_client() -> MongoClient:
    """
    Get a non cached mongo client
    """
    return MongoClient(
        f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority&appName=Cluster0"
    )


@cache
def get_client() -> MongoClient:
    """
    Get a cached mongo client
    """
    return _get_client()


def get_single_listing(listing_id: str) -> dict | None:
    """
    Get a single listing object. Does not include matching ppr data
    """
    return getattr(get_client().eppr, LISTING_PPR_DATA_OPTION).find_one(
        {"_id": ObjectId(listing_id)}
    )


def get_single_ppr(ppr_id: str) -> dict | None:
    """
    Get a single ppr object, includes matched data if available.
    """
    return getattr(get_client().eppr, MATCHED_WITH_PPR_DATA_OPTION).find_one(
        {"_id": ObjectId(ppr_id)}
    )


def get_time_property(data_option: str) -> str:
    """
    Given the type of data we're looking at, return the time field we want to use.

    :param data_option: The type of data we want to work with, listing or matched ppr
    """
    return "ppr_sale_date" if data_option == "matchedWithPPR" else "published_date"


def get_price_property(data_option: str) -> str:
    """
    Given the type of data we're looking at, return the price field we want to use.

    :param data_option: The type of data we want to work with, listing or matched ppr
    """
    if data_option == "PPRPrice":
        return "ppr_price"
    elif data_option == "matchedWithPPR":
        return "ppr_price"
    elif data_option == "allHistoricalListings":
        return "price"

    raise ValueError(f'data_option "{data_option}" not recognised')


def get_collection_name(data_option: str) -> str:
    """
    Given the type of data we're looking at, return the time collection name we want to use.

    :param data_option: The type of data we want to work with, listing or matched ppr
    """
    if data_option == "PPRPrice":
        return PPR_DATA_OPTION
    elif data_option == "matchedWithPPR":
        return MATCHED_WITH_PPR_DATA_OPTION
    elif data_option == "allHistoricalListings":
        return LISTING_PPR_DATA_OPTION

    raise ValueError(f'data_option "{data_option}" not recognised')


def get_poly(
    min_latitude: float, max_latitude: float, min_longitude: float, max_longitude: float
) -> dict:
    """
    Given min and max lat and lng, get the mongodb polygon to use for matching.

    :param min_latitude:
    :param max_latitude:
    :param min_longitude:
    :param max_longitude:
    """
    return {
        "type": "Polygon",
        "coordinates": [
            [
                [min_longitude, min_latitude],
                [max_longitude, min_latitude],
                [max_longitude, max_latitude],
                [min_longitude, max_latitude],
                [min_longitude, min_latitude],
            ]
        ],
    }


def update_match(pipeline: list, index: int, filter_obj: dict) -> list:
    """
    Given a pipeline, update the matching section at a specified stage index.

    :param pipeline:
    :param index:
    :param filter_obj:
    """
    if filter_obj:
        pipeline[index]["$match"].update(filter_obj)

    return pipeline
