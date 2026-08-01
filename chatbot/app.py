import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
import psycopg2  # Mantendo o seu driver de banco de dados
from google import genai

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Data Assistant - DBT News",
    page_icon="📰",
    layout="wide"
)

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)

# 1. Configuração do Cliente Gemini
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 2. Busca o contexto direto do banco
@st.cache_data(ttl=300)  # Cache de 5 minutos para economizar chamadas ao banco
def buscar_contexto_noticias(limite=15):
    conn = psycopg2.connect(
        host=os.getenv("HOST_DB", "localhost"),
        database=os.getenv("DATABASE_DB", "postgres"),
        user=os.getenv("USER_DB", "postgres"),
        password=os.getenv("PASSWORD_DB", "postgres"),
        port=os.getenv("PORT_DB", "5432")
    )
    cursor = conn.cursor()
    
    # Nome da sua View do dbt
    query = """
        SELECT context 
        FROM marts.mart_ai_context 
        ORDER BY published_at DESC 
        LIMIT %s;
    """
    cursor.execute(query, (limite,))
    rows = cursor.fetchall()
    conn.close()
    
    blocos = [row[0] for row in rows if row[0]]
    return "\n\n====================\n\n".join(blocos)

# --- INTERFACE VISUAL ---
st.title("🤖 Data Assistant - Consumo de View dbt")
st.caption("Interface de consumo interativa para o pipeline de Engenharia de Dados")

# Sidebar com status do banco de dados
with st.sidebar:
    st.header("⚙️ Status do Pipeline")
    try:
        contexto_noticias = buscar_contexto_noticias(limite=15)
        st.success("Conectado à View do dbt!")
        st.metric(label="Notícias Carregadas", value=15)
    except Exception as e:
        st.error(f"Erro na conexão com o Banco: {e}")
        contexto_noticias = None

    if st.button("Limpar Histórico de Chat"):
        st.session_state.messages = []
        st.rerun()

# Inicializa o histórico de mensagens da sessão
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores do chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input de mensagem do usuário
if user_input := st.chat_input("Pergunte algo sobre as notícias tratadas pelo dbt..."):
    if not contexto_noticias:
        st.error("Não foi possível carregar o contexto do banco de dados.")
    else:
        # Adiciona e exibe mensagem do usuário
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Monta o prompt
        prompt = f"""
        Você é um assistente analista de dados. Responda à pergunta do usuário utilizando estritamente 
        as informações do contexto abaixo, geradas pela pipeline de dados do dbt.

        --- CONTEXTO DAS NOTÍCIAS ---
        {contexto_noticias}
        --- FIM DO CONTEXTO ---

        Pergunta do usuário: {user_input}
        """

        # Resposta da LLM
        with st.chat_message("assistant"):
            with st.spinner("Analisando notícias..."):
                try:
                    client = get_gemini_client()
                    # MANTIDO O MESMO MODELO QUE VOCÊ JÁ VALIDOU:
                    response = client.models.generate_content(
                        model="models/gemini-3.1-flash-lite",
                        contents=prompt,
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Erro ao processar resposta: {e}")