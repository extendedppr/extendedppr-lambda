import datetime

from eppr.utils import (
    is_default_beds,
)


def get_bed_filter(min_beds: int, max_beds: int) -> dict | None:
    if not is_default_beds(min_beds, max_beds):
        return {"beds": {"$gte": min_beds, "$lte": max_beds}}


def get_county_filter(counties: str) -> dict | None:
    """

    :param counties:
    """
    if not counties:
        return None
    if "all" not in counties:
        return {"county": {"$in": counties}}


def get_property_type_filter(property_types: str) -> dict | None:
    """

    :param property_types:
    """
    if not property_types:
        return None
    if "all" not in property_types:
        return {"property_type": {"$in": property_types}}


def get_agent_filter(agents: str) -> dict | None:
    """

    :param agents:
    """
    if not agents:
        return None
    if "all" not in agents:
        return {"clean_agent": {"$in": agents}}


def get_time_range_filter(field_name: str, min_year: int, max_year: int) -> dict:
    """

    :param field_name:
    :param min_year:
    :param max_year:
    """
    # TODO: instead of taking the field name take the data type and get the field name
    return {
        field_name: {
            "$gte": datetime.datetime(int(min_year), 1, 1),
            "$lte": datetime.datetime(int(max_year), 12, 31),
        }
    }
