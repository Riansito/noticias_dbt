import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

sys.path.append(str(BASE_DIR))

from database.connection import engine
from rag.embedding_service import generate_embedding


def process_embeddings() -> None:
    """
    Gera e salva os embeddings noticia por noticia no PostgreSQL.
    """
    select_query = text("""
        SELECT
            m.news_key,
            m.context
        FROM marts.mart_ai_context m
        LEFT JOIN news_embeddings e
            ON m.news_key = e.news_key
        WHERE e.news_key IS NULL;
    """)

    insert_query = text("""
        INSERT INTO news_embeddings (
            news_key,
            context,
            embedding
        )
        VALUES (
            :news_key,
            :context,
            CAST(:embedding AS JSONB)
        );
    """)

    with engine.connect() as conn:
        rows = conn.execute(select_query).fetchall()

    total = len(rows)
    print(f"{total} notícias pendentes para geração de embedding.")

    if not rows:
        return

    records_to_insert = []
    
    for idx, row in enumerate(rows, start=1):
        try:
            embedding = generate_embedding(row.context)

            records_to_insert.append({
                "news_key": row.news_key,
                "context": row.context,
                "embedding": json.dumps(embedding),
            })

            if idx % 50 == 0 or idx == total:
                # Salva no banco a cada 50 itens processados
                with engine.begin() as conn:
                    conn.execute(insert_query, records_to_insert)
                print(f"Progresso: {idx}/{total} notícias processadas e salvas.")
                records_to_insert.clear()

            # Pausa curta de 50ms para respeitar a API
            time.sleep(0.05)

        except Exception as e:
            print(f"Erro ao processar noticia news_key={row.news_key}: {e}")
            # Salva o que já foi gerado até o momento do erro
            if records_to_insert:
                with engine.begin() as conn:
                    conn.execute(insert_query, records_to_insert)
            raise e

    print("Embeddings gerados e salvos com sucesso!")


if __name__ == "__main__":
    process_embeddings()