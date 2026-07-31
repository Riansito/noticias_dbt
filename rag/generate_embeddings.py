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
from rag.embedding_service import generate_embeddings_batch


def chunk_list(lst, batch_size):
    """Divide uma lista em pedaços de tamanho fixo."""
    for i in range(0, len(lst), batch_size):
        yield lst[i : i + batch_size]


def process_embeddings() -> None:
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

    # Reduzido de 25 para 5 para não estourar o limite de payload/tokens das matérias
    BATCH_SIZE = 5
    processed_count = 0

    for chunk in chunk_list(rows, BATCH_SIZE):
        texts = [r.context for r in chunk]
        embeddings = None

        for attempt in range(1, 4):
            try:
                embeddings = generate_embeddings_batch(texts)
                break
            except Exception as e:
                print(
                    f"⚠️ Erro no lote (tentativa {attempt}/3): {e}. Aguardando 3s..."
                )
                time.sleep(3)

        if not embeddings:
            print("❌ Não foi possível gerar embeddings para este lote. Pulei.")
            continue

        records_to_insert = [
            {
                "news_key": r.news_key,
                "context": r.context,
                "embedding": json.dumps(emb),
            }
            for r, emb in zip(chunk, embeddings)
        ]

        with engine.begin() as conn:
            conn.execute(insert_query, records_to_insert)

        processed_count += len(chunk)
        print(f"Progresso: {processed_count}/{total} notícias salvas.")
        time.sleep(0.5)

    print("✨ Processamento finalizado com sucesso!")


if __name__ == "__main__":
    process_embeddings()