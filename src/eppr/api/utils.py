from flask import make_response


def convert_response(raw_response: dict):
    """
    wrapper around to convert normal lambda responses to flask responses
    """
    response = make_response(
        raw_response.get("body", {}), raw_response.get("statusCode", 200)
    )
    response.headers = raw_response.get("headers", {})
    return response
