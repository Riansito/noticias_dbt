import os
from pathlib import Path

from dotenv import load_dotenv

from config.logger import logger
from ingestion._1_extract_news import extract_news
from ingestion._2_load_neon import load_raw

# Carrega variáveis de ambiente
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)

api_key = os.getenv("API_KEY")
url = "https://api.apitube.io/v1/news/everything"


def run_pipeline(url, api_key):
    logger.info("Iniciando extração de notícias...")
    data_extracted = extract_news(url, api_key)
    logger.info(
        f"{len(data_extracted)} notícias extraídas. Iniciando carregamento no banco..."
    )
    load_raw(data_extracted)
    logger.info("Pipeline de ingestão finalizada com sucesso.")


if __name__ == "__main__":
    run_pipeline(url, api_key)
