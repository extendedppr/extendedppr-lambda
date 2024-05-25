import copy
import datetime
import json
import math

from unittest import TestCase

from bson import ObjectId

from eppr.utils import (
    get_basic_params,
    convert_to_json,
    construct_data_response,
)
from eppr.mongo.utils import (
    get_time_property,
    get_price_property,
    get_collection_name,
    get_poly,
    update_match,
)
from eppr.settings import MATCHED_WITH_PPR_DATA_OPTION, LISTING_PPR_DATA_OPTION


class TestUtils(TestCase):

    def test_get_basic_params(self):
        self.assertEqual(
            get_basic_params(
                {"minLat": 0, "maxLat": 0.1, "minLng": 0.2, "maxLng": 0.3}
            ),
            (None, None, None, None, None, 0, 100, 0.0, 0.1, 0.2, 0.3),
        )

        self.assertEqual(
            get_basic_params(
                {
                    "filterCounties": "counties,2",
                    "filterAgents": "agents",
                    "filterPropertyTypes": "property_types",
                    "minDate": "mindate",
                    "maxDate": "maxdate",
                    "minLat": 0,
                    "maxLat": 0.1,
                    "minLng": 0.2,
                    "maxLng": 0.3,
                }
            ),
            (
                ["counties", "2"],
                ["agents"],
                ["property_types"],
                "mindate",
                "maxdate",
                0,
                100,
                0.0,
                0.1,
                0.2,
                0.3,
            ),
        )

    def test_construct_data_response(self):
        self.assertEqual(
            construct_data_response(["some data"]),
            {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET",
                    "X-Requested-With": "*",
                    "Content-Type": "application/json",
                },
                "body": '["some data"]',
            },
        )

    def test_convert_to_json(self):
        self.assertEqual(
            json.dumps({"nan": math.nan}, default=convert_to_json), '{"nan": NaN}'
        )
        self.assertEqual(
            json.dumps({"dt": datetime.datetime(2024, 1, 1)}, default=convert_to_json),
            '{"dt": "2024-01-01 00:00:00"}',
        )
        self.assertEqual(
            json.dumps(
                {"bson": ObjectId("507f1f77bcf86cd799439011")}, default=convert_to_json
            ),
            '{"bson": "507f1f77bcf86cd799439011"}',
        )

    def test_update_match(self):
        pipeline = [{"$match": {1: 1}}, {"$match": {2: 2}}]

        self.assertEqual(
            update_match(copy.deepcopy(pipeline), 0, {"a": "a"}),
            [{"$match": {1: 1, "a": "a"}}, {"$match": {2: 2}}],
        )
        self.assertEqual(
            update_match(copy.deepcopy(pipeline), 1, {"a": "a"}),
            [{"$match": {1: 1}}, {"$match": {2: 2, "a": "a"}}],
        )

    def test_get_poly(self):
        self.assertEqual(
            get_poly(0, 1, 2, 3),
            {
                "type": "Polygon",
                "coordinates": [[[2, 0], [3, 0], [3, 1], [2, 1], [2, 0]]],
            },
        )

    def test_get_collection_name(self):
        self.assertEqual(
            get_collection_name("matchedWithPPR"), MATCHED_WITH_PPR_DATA_OPTION
        )
        self.assertEqual(get_collection_name("anythingelse"), LISTING_PPR_DATA_OPTION)

    def test_get_price_property(self):
        self.assertEqual(get_price_property("matchedWithPPR"), "ppr_price")
        self.assertEqual(get_price_property("anythingelse"), "price")

    def test_get_time_property(self):
        self.assertEqual(get_time_property("matchedWithPPR"), "ppr_sale_date")
        self.assertEqual(get_time_property("anythingelse"), "published_date")
