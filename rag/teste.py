import os
from dotenv import load_dotenv
from google import genai
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg2  # Ou sqlite3, duckdb, google.cloud.bigquery, etc.
from google import genai

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(env_path)
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- Modelos disponíveis para texto/chat ---")
for m in client.models.list():
    if m.supported_actions and "generateContent" in m.supported_actions:
        print(f"ID: {m.name}")