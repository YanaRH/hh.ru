import sys
from unittest.mock import patch, Mock
from argparse import Namespace
import pytest
import logging
from hh_parser.main import main, setup_logging


class TestMain:
    """Тесты для main.py."""

    @patch('hh_parser.main.HHParser')
    @patch('hh_parser.main.CSVExporter')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main(self, mock_args, mock_exporter, mock_parser):
        """Тест функции main."""
        mock_args.return_value = Namespace(query="test", pages=1, output="test.csv")
        mock_parser_instance = Mock()
        mock_parser_instance.search_vacancies.return_value = []
        mock_parser.return_value = mock_parser_instance

        with patch('sys.argv', ['script.py', 'test']):
            main()

        mock_parser_instance.search_vacancies.assert_called_once()
        mock_exporter.return_value.export.assert_called_once()

    def test_setup_logging(self, caplog):
        """Тест настройки логирования."""
        caplog.set_level(logging.INFO)
        setup_logging()

        # Проверяем что логирование настроено
        assert caplog.handler.level == logging.INFO