import unittest
from unittest.mock import MagicMock, patch

from ingestion._1_extract_news import extract_news
from ingestion._2_load_neon import load_raw
from ingestion._3_pipeline import run_pipeline


class TestIngestion(unittest.TestCase):
    @patch("ingestion._1_extract_news.requests.get")
    def test_extract_news(self, mock_get):
        # Configura o mock da API
        mock_response = MagicMock()
        mock_response.json.return_value = {"results": [{"id": 1, "title": "Test"}]}
        mock_get.return_value = mock_response

        # Chama a função
        results = extract_news("http://test.com", "fake_key")

        # Verifica retorno e chamadas
        self.assertEqual(results, [{"id": 1, "title": "Test"}])
        mock_get.assert_called_once_with(
            "http://test.com", headers={"X-API-Key": "fake_key"}
        )

    @patch("ingestion._2_load_neon.engine.begin")
    def test_load_raw_with_data(self, mock_engine_begin):
        # Cria dados fictícios
        fake_news = [{"id": 1, "title": "News 1"}, {"id": 2, "title": "News 2"}]

        # Configura o mock do context manager (with engine.begin() as conn)
        mock_conn = MagicMock()
        mock_context_manager = MagicMock()
        mock_context_manager.__enter__.return_value = mock_conn
        mock_engine_begin.return_value = mock_context_manager

        # Chama a função
        load_raw(fake_news)

        # Verifica se o execute foi chamado com a query e as linhas
        mock_conn.execute.assert_called_once()
        args, _ = mock_conn.execute.call_args
        rows = args[1]
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["news_id"], 1)

    @patch("ingestion._2_load_neon.engine.begin")
    def test_load_raw_empty(self, mock_engine_begin):
        # Chama com lista vazia
        load_raw([])
        # Certifica-se de que nada do banco foi executado
        mock_engine_begin.assert_not_called()

    @patch("ingestion._3_pipeline.load_raw")
    @patch("ingestion._3_pipeline.extract_news")
    def test_run_pipeline(self, mock_extract, mock_load):
        # Configura o retorno da extração simulada
        mock_extract.return_value = [{"id": 99, "title": "Mocked News"}]

        # Chama a função principal
        run_pipeline("url", "key")

        # Verifica fluxo da pipeline
        mock_extract.assert_called_once_with("url", "key")
        mock_load.assert_called_once_with([{"id": 99, "title": "Mocked News"}])
