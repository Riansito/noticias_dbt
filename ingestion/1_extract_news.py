import requests

def extract_news(api_url, api_key):
    response = requests.get(
        "https://api.apitube.io/v1/news/everything",
        headers={"X-API-Key": "api_live_JXdxQuMpCmQYZUT9GXfEsYAVSHcjVbPj9MNDWTCyKZuD8ZYAzAkPfovdHL"},
    )

    response.json()