import json

# Carrega o arquivo .env
import sys
from pathlib import Path

from sqlalchemy import text

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))


from database.connection import engine


def load_raw(news: list[dict]) -> None:
    """
    Carrega as notícias na camada RAW.

    Caso a notícia já exista, ela é ignorada.
    """

    if not news:
        return

    query = text("""
        INSERT INTO raw.news (
            news_id,
            payload
        )
        VALUES (
            :news_id,
            CAST(:payload AS JSONB)
        )
        ON CONFLICT (news_id)
        DO NOTHING;
    """)

    from ingestion.schemas import NewsItem
    from pydantic import ValidationError

    rows = []
    for item in news:
        try:
            # Valida e converte o item pelo modelo
            valid_item = NewsItem(**item)
            rows.append(
                {
                    "news_id": valid_item.id,
                    "payload": valid_item.model_dump_json(),
                }
            )
        except ValidationError as e:
            print(f"Erro de validação no item {item.get('id')}: {e}")
            continue

    if not rows:
        return

    with engine.begin() as conn:
        conn.execute(query, rows)
