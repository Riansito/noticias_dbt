import os
from pathlib import Path

from dotenv import load_dotenv

# Define o caminho base do projeto e carrega o .env
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

# Configurações do Banco de Dados
DB_HOST = os.getenv("HOST_DB", "localhost")
DB_DATABASE = os.getenv("DATABASE_DB", "postgres")
DB_USER = os.getenv("USER_DB", "postgres")
DB_PASSWORD = os.getenv("PASSWORD_DB", "postgres")
DB_PORT = os.getenv("PORT_DB", "5432")

# Configurações do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
