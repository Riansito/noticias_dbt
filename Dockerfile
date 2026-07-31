FROM apache/airflow:3.1.7

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

USER airflow

COPY airflow/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /opt/airflow/project