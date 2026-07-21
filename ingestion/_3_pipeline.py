from _1_extract_news import extract_news
from _2_load_neon import load_raw

from pathlib import Path
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)

api_key = os.getenv("API_KEY")
url = "https://api.apitube.io/v1/news/everything"

data_extracted = extract_news(url, api_key)
load_raw(data_extracted)
