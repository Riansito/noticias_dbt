import os
import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

sys.path.append(str(BASE_DIR))

from rag.llm import generate_rag_response


def main():
    print("=== ASSISTENTE DE NOTÍCIAS RAG ===")
    print("Digite sua pergunta abaixo ou digite 'sair' para encerrar.\n")

    while True:
        try:
            user_input = input("Pergunta > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando...")
            break

        if user_input.lower() in ["sair", "exit", "quit"]:
            print("Até logo!")
            break

        if not user_input:
            continue

        print("\nBuscando contexto e processando com o LLM...\n")
        resposta = generate_rag_response(user_input)
        print(f"Resposta:\n{resposta}\n")
        print("=" * 60)


if __name__ == "__main__":
    main()