import unittest
from unittest.mock import MagicMock, patch

from chatbot.app import buscar_contexto_noticias


class TestApp(unittest.TestCase):
    def setUp(self):
        buscar_contexto_noticias.clear()

    @patch("chatbot.app.psycopg2.connect")
    def test_buscar_contexto_noticias_sucesso(self, mock_connect):
        # Configura o mock do banco de dados
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simula o retorno de fetchall
        mock_cursor.fetchall.return_value = [("Notícia 1",), ("Notícia 2",)]

        # Chama a função
        resultado = buscar_contexto_noticias(limite=2)

        # Asserts
        self.assertEqual(resultado, "Notícia 1\n\n====================\n\nNotícia 2")
        mock_connect.assert_called_once()
        mock_conn.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("chatbot.app.psycopg2.connect")
    def test_buscar_contexto_noticias_vazio(self, mock_connect):
        # Configura o mock do banco de dados
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Simula o retorno vazio de fetchall
        mock_cursor.fetchall.return_value = []

        # Chama a função
        resultado = buscar_contexto_noticias(limite=2)

        # Asserts
        self.assertEqual(resultado, "")
        mock_connect.assert_called_once()
