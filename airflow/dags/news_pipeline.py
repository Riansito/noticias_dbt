from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="news_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="0 */6 * * *",
    catchup=False,
    tags=["news", "dbt", "rag"],
) as dag:

    ingest_news = BashOperator(
        task_id="ingest_news",
        bash_command="""
        cd /opt/airflow/project &&
        python ingestion/_3_pipeline.py
        """
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /opt/airflow/project/dbt/news_rag &&
        dbt run --profiles-dir /opt/airflow/project/dbt
        """
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        cd /opt/airflow/project/dbt/news_rag &&
        dbt test --profiles-dir /opt/airflow/project/dbt
        """
    )

    generate_embeddings = BashOperator(
        task_id="generate_embeddings",
        bash_command="""
        cd /opt/airflow/project &&
        python rag/generate_embeddings.py
        """
    )

    # Fluxo do pipeline: Ingestão -> dbt Run -> dbt Test -> Embeddings
    ingest_news >> dbt_run >> dbt_test >> generate_embeddings