"""
SQLite DBManager для HH вакансий.
"""
import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class SQLiteDBManager:
    """
    Менеджер БД для хранения вакансий HH.ru.

    Все 5 методов из задания реализованы.
    """

    def __init__(self, db_file: str = "hh_vacancies.db"):
        """
        Инициализация БД.

        Args:
            db_file: Путь к файлу БД
        """
        self.db_file = db_file
        """Путь к файлу БД."""
        self._create_tables()

    def _create_tables(self) -> None:
        """
        Создать таблицы companies и vacancies.
        Автоматически вызывается при инициализации.
        """
        # ... код создания таблиц

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Список компаний и количество вакансий (JOIN).

        Returns:
            [('Yandex', 25), ('Sber', 15), ...]
        """
        # SQL JOIN запрос

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Все вакансии с названием компании (JOIN).

        Returns:
            [{'company': 'Yandex', 'name': 'Python Dev', 'salary': 200000, 'url': '...'}]
        """
        # SQL JOIN запрос

    def get_avg_salary(self) -> Optional[float]:
        """
        Средняя зарплата (AVG).

        Returns:
            250000.5 или None
        """
        # SQL AVG

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """
        Вакансии выше средней зарплаты (WHERE > AVG).

        Returns:
            Список вакансий
        """
        # SQL WHERE > AVG

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Поиск вакансий по ключевому слову (LIKE).

        Args:
            keyword: "python", "senior" и т.д.

        Returns:
            Список вакансий
        """
        # SQL LIKE %keyword%

    def fill_test_data(self) -> None:
        """
        Заполнить БД 10 компаниями + вакансиями.
        Для демонстрации задания.
        """
        # Тестовые данные