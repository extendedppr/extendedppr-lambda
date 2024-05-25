import os
import json
from collections import defaultdict

from dotenv import find_dotenv, load_dotenv
import boto3


if find_dotenv():
    load_dotenv()


def get_secret(secret_name):
    secret_client = boto3.client("secretsmanager")

    try:
        return json.loads(
            secret_client.get_secret_value(SecretId=secret_name)["SecretString"]
        )
    except:
        print(f'ERROR: Could not get secret "{secret_name}"')
        return defaultdict(str)


mongo_creds = get_secret("mongo_creds")

MONGO_USER = os.getenv("MONGO_USER", mongo_creds["MONGO_USER"])
MONGO_PASS = os.getenv("MONGO_PASS", mongo_creds["MONGO_PASS"])
MONGO_HOST = os.getenv("MONGO_HOST", mongo_creds["MONGO_HOST"])

if not MONGO_USER or not MONGO_PASS or not MONGO_HOST:
    print("WARNING: Not all Mongo details not set (MONGO_HOST, MONGO_USER, MONGO_PASS)")

MATCHED_WITH_PPR_DATA_OPTION = os.getenv("MATCHED_WITH_PPR_DATA_OPTION", "ppr_data")
LISTING_PPR_DATA_OPTION = os.getenv("LISTING_PPR_DATA_OPTION", "listing_data")
