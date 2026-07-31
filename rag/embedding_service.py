import os
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

sys.path.append(str(BASE_DIR))

API_KEY = os.getenv("GEMINI_API_KEY")


def generate_embedding(text: str) -> list[float]:
    """
    Gera embedding utilizando a API do Gemini (text-embedding-004).
    Tamanho do vetor retornado: 768
    """
    if not text:
        return []

    # Endpoint oficial usando o parâmetro key
    url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={API_KEY}"

    payload = {
        "model": "models/text-embedding-004",
        "content": {
            "parts": [{"text": text}]
        }
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    # Caso a chave exija cabeçalho Bearer (contas institucionais)
    if response.status_code in (401, 403):
        url_no_key = "https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent"
        headers["Authorization"] = f"Bearer {API_KEY}"
        response = requests.post(url_no_key, json=payload, headers=headers)

    response.raise_for_status()

    data = response.json()
    return data["embedding"]["values"]