SAMPLE_SIZE = 1000

RESPONSE_HEADERS = {
    "Access-Control-Allow-Headers": (
        "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,"
        "Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers"
    ),
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "X-Requested-With": "*",
    "Content-Type": "application/json",
}

EMPTY_GEOJSON = {"type": "FeatureCollection", "features": []}
