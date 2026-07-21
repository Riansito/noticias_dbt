import json

from sqlalchemy import text

# Carrega o arquivo .env
import os
from pathlib import Path
from dotenv import load_dotenv
import sys
from pathlib import Path

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

    rows = [
        {
            "news_id": item["id"],
            "payload": json.dumps(item),
        }
        for item in news
    ]

    with engine.begin() as conn:
        conn.execute(query, rows)