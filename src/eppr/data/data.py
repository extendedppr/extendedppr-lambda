import sys
from bson.objectid import ObjectId

from eppr.mongo.utils import (
    get_time_property,
    get_price_property,
    get_collection_name,
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


def get_data(
    counties: str,
    agents: str,
    property_types: str,
    min_year: int,
    max_year: int,
    min_beds: int,
    max_beds: int,
    min_price: int,
    max_price: int,
    data_option: str,
    marker: str | None,
    page_size: int,
):

    if marker:
        object_id_min = ObjectId(marker)
    else:
        object_id_min = ObjectId("000000000000000000000000")

    pipeline = [
        {"$match": {"_id": {"$gt": object_id_min}}},
        {"$sort": {"_id": 1}},
        {"$limit": page_size},
    ]

    if not min_year:
        min_year = 1
    if not max_year:
        max_year = 9999
    if not min_beds:
        min_beds = 0
    if not max_beds:
        max_beds = sys.maxsize
    if not min_price:
        min_price = 0
    if not max_price:
        max_price = sys.maxsize

    for filter_obj in [
        get_price_filter(get_price_property(data_option), min_price, max_price),
        get_county_filter(counties),
        get_property_type_filter(property_types),
        get_agent_filter(agents),
        get_time_range_filter(get_time_property(data_option), min_year, max_year),
        get_bed_filter(min_beds, max_beds),
    ]:
        pipeline = update_match(pipeline, 0, filter_obj)

    return list(aggregate(get_collection_name(data_option), pipeline))
