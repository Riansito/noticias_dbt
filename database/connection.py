import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


# Carrega o arquivo .env
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)


def get_engine() -> Engine:
    """
    Cria e retorna o engine de conexão com o Neon PostgreSQL.
    """

    user = os.getenv("USER_DB")
    password = os.getenv("PASSWORD_DB")
    host = os.getenv("HOST_DB")
    port = os.getenv("PORT_DB", "5432")
    database = os.getenv("DATABASE_DB")

    database_url = (
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        "?sslmode=require"
    )

    return create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


engine = get_engine()