import requests


def extract_news(api_url, api_key):
    response = requests.get(
        api_url,
        headers={"X-API-Key": api_key},
    )

    return response.json()["results"]
