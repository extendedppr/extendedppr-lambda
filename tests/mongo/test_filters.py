import os
import datetime

from unittest import TestCase, skip

from eppr.mongo.filters import (
    get_county_filter,
    get_agent_filter,
    get_property_type_filter,
    get_time_range_filter,
)


class TestFilters(TestCase):

    def test_get_county_filter(self):
        self.assertEqual(get_county_filter(None), None)
        self.assertEqual(get_county_filter(""), None)
        self.assertEqual(get_county_filter(["a", "b"]), {"county": {"$in": ["a", "b"]}})

    def test_get_agent_filter(self):
        self.assertEqual(get_agent_filter(None), None)
        self.assertEqual(get_agent_filter(""), None)
        self.assertEqual(
            get_agent_filter(["a", "b"]), {"clean_agent": {"$in": ["a", "b"]}}
        )

    def test_get_property_type_filter(self):
        self.assertEqual(get_property_type_filter(None), None)
        self.assertEqual(get_property_type_filter(""), None)
        self.assertEqual(
            get_property_type_filter(["a", "b"]), {"property_type": {"$in": ["a", "b"]}}
        )

    def test_get_time_range_filter(self):
        self.assertEqual(
            get_time_range_filter("published_date", 1, 2),
            {
                "published_date": {
                    "$gte": datetime.datetime(1, 1, 1, 0, 0),
                    "$lte": datetime.datetime(2, 12, 31, 0, 0),
                }
            },
        )
