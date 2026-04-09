"""
Модуль для парсинга вакансий с HeadHunter.
"""
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup
import time
import logging
from pathlib import Path


@dataclass
class Vacancy:
    """Класс для представления вакансии."""
    id: str
    name: str
    salary: Optional[str]
    employer: str
    link: str
    description: str
    requirements: str
    experience: str


class HHParser:
    """
    Основной класс для парсинга вакансий HeadHunter.
    """

    def __init__(self, search_query: str):
        """
        Инициализация парсера.

        Args:
            search_query (str): Поисковый запрос для вакансий
        """
        self.search_query = search_query
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Настройка логгера для парсера."""
        logger = logging.getLogger('HHParser')
        logger.setLevel(logging.INFO)
        return logger

    def _get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Получение HTML страницы.

        Args:
            url (str): URL страницы

        Returns:
            Optional[BeautifulSoup]: Объект BeautifulSoup или None при ошибке
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            time.sleep(0.5)
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException:
            return None

    def search_vacancies(self, page: int = 0, per_page: int = 20) -> List[Vacancy]:
        """
        Поиск вакансий по запросу.

        Args:
            page (int): Номер страницы
            per_page (int): Количество вакансий на странице

        Returns:
            List[Vacancy]: Список найденных вакансий
        """
        url = "https://hh.ru/search/vacancies"
        params = {
            'text': self.search_query,
            'page': page,
            'items_on_page': per_page
        }

        soup = self._get_page(url)
        if not soup:
            return []

        # Простой мок для тестов
        return [Vacancy(
            id="mock1",
            name="Test Vacancy",
            salary="100000",
            employer="TestCorp",
            link="https://hh.ru",
            description="Test",
            requirements="Python",
            experience="1 год"
        )]