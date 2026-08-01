# 📰 News Analytics Pipeline + AI Assistant

> Pipeline completo de Engenharia de Dados para coleta, transformação e disponibilização de notícias através de um Data Warehouse modelado em estrela e consumido por um assistente de IA utilizando Google Gemini.

---

# 📖 Introdução

Atualmente milhares de notícias são publicadas diariamente por diferentes portais, tornando difícil centralizar, organizar e consultar essas informações de forma eficiente.

Grande parte das APIs de notícias retorna documentos JSON complexos, altamente aninhados e pouco adequados para análises, dashboards ou aplicações inteligentes.

Este projeto resolve esse problema construindo um pipeline moderno de Engenharia de Dados que transforma dados brutos em um Data Warehouse organizado, permitindo consultas analíticas e utilização por aplicações de Inteligência Artificial.

O pipeline realiza desde a ingestão automática das notícias até a disponibilização de uma camada otimizada para consumo por um chatbot baseado no Google Gemini.

---

# 🎯 Problema de Negócio

Uma API de notícias fornece informações extremamente ricas, porém em formato JSON aninhado.

Esse formato apresenta diversos desafios:

* Dados duplicados
* Objetos e arrays complexos
* Baixa performance para consultas
* Dificuldade para aplicações de IA
* Pouca padronização
* Difícil integração com ferramentas analíticas

O objetivo deste projeto é transformar esses dados em um modelo dimensional otimizado para consultas analíticas e aplicações inteligentes.

---

# 🚀 Objetivos

O projeto foi desenvolvido para demonstrar um pipeline moderno de Engenharia de Dados utilizando boas práticas do mercado.

Entre os principais objetivos estão:

* Automatizar a ingestão de notícias
* Armazenar os dados brutos
* Construir um Data Warehouse utilizando dbt
* Aplicar testes de qualidade nos dados
* Criar uma camada otimizada para IA
* Disponibilizar um chatbot capaz de responder perguntas utilizando os dados estruturados

---

# 🏗 Arquitetura

```text
                    News API
                       │
                       ▼
             Python Ingestion
                       │
                       ▼
              PostgreSQL (Raw)
                       │
                       ▼
                  Apache Airflow
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
         dbt Run              dbt Test
            │
            ▼
      Data Warehouse
            │
    ┌───────┴────────┐
    ▼                ▼
 Fact Tables    Dimensions
            │
            ▼
      mart_ai_context
            │
            ▼
     Google Gemini Chatbot
            │
            ▼
   Respostas em linguagem natural
```
Imagem da arquitetura:
<img width="1672" height="941" alt="ChatGPT Image 1 de ago  de 2026, 15_49_37" src="https://github.com/user-attachments/assets/83a50022-e1e7-49cf-b301-cc2b5873f7c7" />

---

# ⚙ Tecnologias Utilizadas

### Linguagens

* Python
* SQL

### Orquestração

* Apache Airflow

### Transformação

* dbt

### Banco de Dados

* PostgreSQL (Neon)

### Containers

* Docker
* Docker Compose

### Inteligência Artificial

* Google Gemini

### Bibliotecas

* Pandas
* Requests
* SQLAlchemy
* Psycopg2

---

# 📂 Estrutura do Projeto

```text
news_pipeline/

│
├── airflow/
│   ├── dags/
│   ├── plugins/
│   └── requirements.txt
│
├── dbt/
│   └── news_rag/
│       ├── models/
│       │
│       ├── stage/
│       ├── intermediate/
│       ├── marts/
│       ├── tests/
│       └── macros/
│
├── ingestion/
│
├── chatbot/
│
├── docker-compose.yml
│
└── README.md
```

---

# 📊 Modelagem Dimensional

O projeto utiliza modelagem estrela (Star Schema).

## Fact

* fact_news

## Dimensões

* dim_author
* dim_category
* dim_topic
* dim_source
* dim_sentiment
* dim_language
* dim_industry

## Bridges

* bridge_news_category
* bridge_news_topic
* bridge_news_industry

## Camada para IA

* mart_ai_context

---

# 🔄 Pipeline

## 1. Ingestão

Um processo em Python consome a API de notícias.

Cada resposta é armazenada em sua forma original no PostgreSQL.

Nenhuma transformação é realizada nesta etapa.

---

## 2. Stage

O dbt realiza:

* extração do JSON
* normalização
* tratamento de URLs
* deduplicação
* padronização dos dados

---

## 3. Camada Intermediária

Nesta etapa são construídas todas as dimensões e tabelas bridge.

Também são criadas as chaves substitutas (Surrogate Keys).

---

## 4. Camada Analítica

A tabela fato é construída relacionando todas as dimensões.

Essa camada representa o Data Warehouse principal do projeto.

---

## 5. Camada para IA

A view `mart_ai_context` reúne todas as informações relevantes em um único registro textual.

Ela consolida:

* título
* descrição
* resumo
* autor
* fonte
* país
* categorias
* tópicos
* indústrias
* sentimento

Essa estrutura simplifica o consumo por aplicações de IA.

---

# 🤖 Assistente Inteligente

O projeto possui um chatbot desenvolvido em Python utilizando Google Gemini.

Ao receber uma pergunta do usuário, a aplicação:

1. interpreta a pergunta;
2. consulta a view `mart_ai_context`;
3. recupera os dados relevantes;
4. envia o contexto ao Gemini;
5. retorna uma resposta em linguagem natural.

Dessa forma, o modelo responde com base nas informações armazenadas no Data Warehouse, reduzindo alucinações e tornando as respostas mais consistentes.
<img width="1917" height="903" alt="Captura de tela 2026-08-01 160827" src="https://github.com/user-attachments/assets/75309863-e141-4038-b29c-451fa518676c" />

---

# ✅ Qualidade dos Dados

O projeto utiliza diversos testes implementados no dbt.

Entre eles:

* Unicidade
* Valores nulos
* Integridade referencial
* Datas válidas
* URLs válidas
* Duplicidade de notícias

Todos os testes são executados automaticamente pelo Airflow após cada transformação.

---

# ▶ Como executar

## Clone o projeto

```bash
git clone <repositorio>
```

## Suba os containers

```bash
docker compose up -d
```

## Execute o pipeline

O Airflow será responsável por:

* executar a ingestão;
* executar o dbt run;
* executar o dbt test.

---

## Executar o chatbot

```bash
python chatbot/app.py
```

Faça perguntas como:

* "Quais notícias falam sobre Inteligência Artificial?"

* "Mostre notícias positivas sobre tecnologia."

* "Quais empresas apareceram nas notícias de hoje?"

* "Quais notícias vieram dos Estados Unidos?"

---

# 📈 Melhorias Futuras

* Implementação de RAG com embeddings vetoriais
* Busca semântica utilizando pgvector
* API REST para consulta das notícias
* Dashboard em Power BI
* Monitoramento com Prometheus e Grafana
* CI/CD utilizando GitHub Actions
* Deploy em ambiente cloud
* Cache de consultas utilizando Redis

---

# 👨‍💻 Autor

**Rian**

Estudante de Sistemas de Informação na UFPB, com foco em Engenharia de Dados, Analytics e Inteligência Artificial.

Este projeto foi desenvolvido com o objetivo de consolidar conhecimentos em pipelines de dados modernos, modelagem analítica e integração com modelos de IA generativa, simulando uma arquitetura próxima à utilizada em ambientes de produção.
