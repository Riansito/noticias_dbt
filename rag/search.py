import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

sys.path.append(str(BASE_DIR))

from database.connection import engine
from rag.embedding_service import generate_embedding


def search_similar_news(query: str, top_k: int = 5) -> list[dict]:
    """
    Gera o embedding da query e busca as noticias mais similares no banco.
    """
    query_vector = generate_embedding(query)

    # Consulta PostgreSQL usando pgvector
    search_sql = text("""
        SELECT 
            news_key,
            context,
            1 - (embedding <=> CAST(:query_vector AS vector)) AS similarity
        FROM news_embeddings
        ORDER BY embedding <=> CAST(:query_vector AS vector)
        LIMIT :top_k;
    """)

    with engine.connect() as conn:
        results = conn.execute(
            search_sql,
            {
                "query_vector": str(query_vector),
                "top_k": top_k
            }
        ).fetchall()

    return [
        {
            "news_key": row.news_key,
            "context": row.context,
            "similarity": row.similarity
        }
        for row in results
    ]