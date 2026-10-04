import logging
import sys


def get_logger(name: str = "noticias_dbt"):
    logger = logging.getLogger(name)

    # Evita adicionar múltiplos handlers se a função for chamada mais de uma vez
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Formato do log
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Handler para o console
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger


# Logger padrão exportado
logger = get_logger()
