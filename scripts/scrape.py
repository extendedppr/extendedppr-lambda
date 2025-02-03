import requests
import json

BASE_URL = "https://e4expolexk.execute-api.eu-west-1.amazonaws.com/api/data/"
DATA_OPTIONS = {
    "PPRPrice",
    "matchedWithPPR",
    "allHistoricalListings",
    "shares",
    "rentals",
}


def main():
    page_size = 10000
    for data_option in DATA_OPTIONS:
        url = f"{BASE_URL}?pageSize={page_size}&dataOption={data_option}"
        data = []
        print(f"\nFetching data for: {data_option}")
        while url:
            r = requests.get(url).json()
            data.extend(r["data"])
            url = r.get("next")
        output_file = f"{data_option}.json"
        with open(output_file, "w") as f:
            json.dump(data, f)
        print(f"Saved {data_option} data to {output_file}")


if __name__ == "__main__":
    main()
