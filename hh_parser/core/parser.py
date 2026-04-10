"""
Парсер вакансий HH.ru.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Vacancy:
    """Модель вакансии."""
    id: str
    """Уникальный ID вакансии."""
    name: str
    """Название вакансии."""
    salary: Optional[str]
    """Зарплата."""
    employer: str
    """Работодатель."""
    link: str
    """Ссылка на вакансию."""


class HHParser:
    """Парсер вакансий HeadHunter."""

    def __init__(self, query: str):
        """
        Инициализация парсера.

        Args:
            query: Поисковый запрос
        """
        self.query = query

    def search_vacancies(self, page: int = 0) -> List[Vacancy]:
        """
        Поиск вакансий.

        Args:
            page: Номер страницы

        Returns:
            Список вакансий
        """
        # Реализация...
        return []