import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg2  # Ou sqlite3, duckdb, google.cloud.bigquery, etc.
from google import genai

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)

# 1. Configuração do Cliente Gemini
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Busca o contexto pré-formatado pelo dbt
def buscar_contexto_noticias(limite=15):
    """
    Consome a coluna 'context' diretamente da view do dbt.
    """
    conn = psycopg2.connect(
        host=os.getenv("HOST_DB", "localhost"),
        database=os.getenv("DATABASE_DB", "postgres"),
        user=os.getenv("USER_DB", "postgres"),
        password=os.getenv("PASSWORD_DB", "postgres"),
        port=os.getenv("PORT_DB", "5432")
    )
    cursor = conn.cursor()
    
    # Nome da sua View tratada no dbt (ajuste o nome da tabela se necessário)
    query = """
        SELECT context 
        FROM marts.mart_ai_context 
        ORDER BY published_at DESC 
        LIMIT %s;
    """
    cursor.execute(query, (limite,))
    rows = cursor.fetchall()
    conn.close()
    
    # Junta todos os blocos de contexto retornados da view
    blocos = [row[0] for row in rows if row[0]]
    return "\n\n====================\n\n".join(blocos)

# 3. Loop do Chat no Terminal
def iniciar_chat():
    print("=" * 60)
    print("🤖 CLI Data Assistant - Consumo da View do dbt")
    print("=" * 60)
    print("Carregando contexto das últimas notícias direto do banco...")
    
    try:
        contexto_noticias = buscar_contexto_noticias(limite=15)
        print("✅ Contexto carregado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao conectar no banco de dados: {e}")
        return

    print("Pergunte algo sobre as notícias (ou digite 'sair' para encerrar):\n")

    while True:
        user_input = input("Você > ")
        if user_input.lower().strip() in ["sair", "exit", "quit"]:
            print("Até logo!")
            break

        if not user_input.strip():
            continue

        prompt = f"""
        Você é um assistente analista de dados. Responda à pergunta do usuário utilizando estritamente 
        as informações do contexto abaixo, geradas pela pipeline de dados do dbt.

        --- CONTEXTO DAS NOTÍCIAS ---
        {contexto_noticias}
        --- FIM DO CONTEXTO ---

        Pergunta do usuário: {user_input}
        """

        try:
            response = client.models.generate_content(
                model="models/gemini-3.1-flash-lite",
                contents=prompt,
            )
            print(f"\nBot > {response.text}\n")
            print("-" * 60)
        except Exception as e:
            print(f"\n❌ Erro ao gerar resposta: {e}\n")

if __name__ == "__main__":
    iniciar_chat()