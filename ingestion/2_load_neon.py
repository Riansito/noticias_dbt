import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine




# Carrega variáveis de ambiente
env_path = Path(__file__).resolve().parent.parent / "config" / ".env"

load_dotenv(env_path)

user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")


# URL de conexão com PostgreSQL
url = (
    f"postgresql://{user}:{password}@{host}/{database}"
    "?sslmode=require&channel_binding=require"
)


def get_engine():
    """
    Cria e retorna o engine de conexão com o banco.

    Returns
    -------
    sqlalchemy.engine.Engine
        Engine de conexão com PostgreSQL.
    """

    logger.info("Criando engine de conexão com o banco.")

    return create_engine(url)


# Instância global do engine
engine = get_engine()


def check_data_validation(df, engine, table_name):
    """
    Realiza validação para evitar inserção de dados duplicados.

    A validação verifica se a data máxima já existente no banco
    também existe no DataFrame atual.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame que será carregado.

    engine : sqlalchemy.engine.Engine
        Engine de conexão com o banco.

    table_name : str
        Nome da tabela de destino.
    """

    logger.info("Validando existência de dados duplicados.")

    # Busca maior data existente na tabela
    max_date = pd.read_sql(
        f'SELECT MAX("Date") AS max_date FROM {table_name}',
        con=engine
    )

    max_date = max_date.iloc[0, 0]

    logger.info(f"Maior data encontrada no banco: {max_date}")

    # Verifica se já existem dados dessa data no DataFrame atual
    if len(df[df["Date"] == max_date]) > 0:

        logger.warning("Dados duplicados identificados.")

        raise ValueError("Dados já existentes no banco!")


def load_data(table_name, df):
    """
    Realiza a carga dos dados no PostgreSQL.

    Etapas:
    - Leitura do parquet
    - Validação de duplicidade
    - Inserção transacional no banco
    - Validação pós-carga

    Parameters
    ----------
    table_name : str
        Nome da tabela de destino.

    file_path : str
        Caminho do arquivo parquet.
    """

    logger.info("Iniciando processo de carga dos dados.")

    try:

        # Validação dos dados
        check_data_validation(df, engine, table_name)

        # Inicia transação
        with engine.begin() as connection:

            logger.info("Inserindo dados no banco.")

            df.to_sql(
                table_name,
                con=connection,
                if_exists="append",
                index=False
            )

        # Validação pós-carga
        total_rows = pd.read_sql(
            f"SELECT COUNT(*) AS total FROM {table_name}",
            con=engine
        )

        total_rows = total_rows.iloc[0, 0]

        logger.info(
            f"Carga concluída com sucesso. "
            f"Tabela '{table_name}' possui {total_rows} registros."
        )

    except Exception as e:

        logger.exception(f"Erro durante o processo de carga: {e}")

        # Relança erro para camada superior
        raise