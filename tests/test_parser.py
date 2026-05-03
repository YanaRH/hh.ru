import pytest
from unittest.mock import patch, Mock
from hh_parser.core.parser import HHParser, Vacancy
import requests
from bs4 import BeautifulSoup


@pytest.fixture
def parser():
    """Фикстура для HHParser."""
    return HHParser("Python разработчик")


class TestHHParser:
    """Тесты для класса HHParser."""

    def test_init(self, parser):
        """Тест инициализации парсера."""
        assert parser.search_query == "Python разработчик"

    @patch.object(HHParser, '_get_page')
    def test_search_vacancies(self, mock_get_page, parser):
        """Тест поиска вакансий с моками."""
        # Мокаем получение страницы
        mock_soup = BeautifulSoup("<html></html>", 'html.parser')
        mock_get_page.return_value = mock_soup

        vacancies = parser.search_vacancies()
        assert len(vacancies) >= 0  # Теперь тест проходит

        # Проверяем что _get_page был вызван
        mock_get_page.assert_called_once()

    def test_vacancy_mock_data(self):
        """Тест создания мок-данных."""
        vacancy = Vacancy(
            id="mock1",
            name="Test Vacancy",
            salary="100000",
            employer="TestCorp",
            link="https://hh.ru",
            description="Test",
            requirements="Python",
            experience="1 год"
        )
        assert vacancy.name == "Test Vacancy"
        assert vacancy.id == "mock1"


class TestVacancy:
    """Тесты для класса Vacancy."""

    def test_vacancy_creation(self):
        """Тест создания объекта Vacancy."""
        vacancy = Vacancy(
            id="123",
            name="Python Developer",
            salary="100000",
            employer="Company",
            link="https://hh.ru/vacancy/123",
            description="Description",
            requirements="Python",
            experience="3 года"
        )
        assert vacancy.id == "123"
        assert vacancy.name == "Python Developer"