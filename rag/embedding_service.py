import os
import sys
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    sys.exit("ERRO: GEMINI_API_KEY não configurada.")

client = genai.Client(api_key=api_key)


def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """Gera embeddings para uma lista de textos em uma única requisição HTTP."""
    response = client.models.embed_content(
        model="text-embedding-004", contents=texts
    )
    return [e.values for e in response.embeddings]