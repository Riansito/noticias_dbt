import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

sys.path.append(str(BASE_DIR))

from rag.search import search_similar_news

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_rag_response(user_query: str) -> str:
    """
    Recupera as notícias mais parecidas e gera uma resposta contextualizada via Gemini.
    """
    relevant_news = search_similar_news(user_query, top_k=5)

    if not relevant_news:
        return "Não foi possível encontrar contexto suficiente no banco de dados para responder."

    context_text = "\n\n---\n\n".join([item["context"] for item in relevant_news])

    system_instruction = (
        "Você é um assistente especialista na análise de notícias.\n"
        "Responda à dúvida do usuário utilizando ESTRITAMENTE as informações trazidas no CONTEXTO abaixo.\n"
        "Se o contexto não contiver a resposta, informe expressamente que não há dados suficientes."
    )

    prompt = f"CONTEXTO RECUPERADO:\n{context_text}\n\nPERGUNTA DO USUÁRIO:\n{user_query}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
        ),
    )

    return response.text