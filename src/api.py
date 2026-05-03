"""
Модуль для взаимодействия с API HeadHunter.
"""

import requests
from typing import Any, Dict, List, Optional


class HHApi:
    """Класс для работы с API HeadHunter."""

    BASE_URL = "https://api.hh.ru"

    def __init__(self) -> None:
        """Инициализация API."""
        self._session = requests.Session()
        self._session.headers.update({"User-Agent": "HHParser/1.0"})

    def get_employer(self, employer_id: str) -> Dict[str, Any]:
        """Получение информации о работодателе.

        Args:
            employer_id: ID работодателя на hh.ru

        Returns:
            Словарь с данными о работодателе
        """
        url = f"{self.BASE_URL}/employers/{employer_id}"
        response = self._session.get(url)
        response.raise_for_status()
        return response.json()

    def get_vacancies(
            self,
            employer_id: str,
            page: int = 0,
            per_page: int = 100
    ) -> Dict[str, Any]:
        """Получение вакансий работодателя.

        Args:
            employer_id: ID работодателя
            page: Номер страницы
            per_page: Количество вакансий на странице

        Returns:
            Словарь с вакансиями
        """
        url = f"{self.BASE_URL}/vacancies"
        params = {
            "employer_id": employer_id,
            "page": page,
            "per_page": per_page
        }
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_all_vacancies(self, employer_id: str) -> List[Dict[str, Any]]:
        """Получение всех вакансий работодателя (с пагинацией).

        Args:
            employer_id: ID работодателя

        Returns:
            Список всех вакансий
        """
        all_vacancies = []
        page = 0

        while True:
            data = self.get_vacancies(employer_id, page=page)
            vacancies = data.get("items", [])
            all_vacancies.extend(vacancies)

            if page >= data.get("pages", 1) - 1:
                break
            page += 1

        return all_vacancies

    def search_employers(self, query: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """Поиск работодателей по названию.

        Args:
            query: Поисковый запрос
            per_page: Количество результатов

        Returns:
            Список найденных работодателей
        """
        url = f"{self.BASE_URL}/employers"
        params = {
            "text": query,
            "per_page": per_page
        }
        response = self._session.get(url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])

    @staticmethod
    def get_employer_id(employer_data: Dict[str, Any]) -> str:
        """Извлечение ID работодателя из данных.

        Args:
            employer_data: Данные работодателя

        Returns:
            ID работодателя
        """
        return employer_data.get("id", "")

    @staticmethod
    def get_employer_name(employer_data: Dict[str, Any]) -> str:
        """Извлечение названия работодателя из данных.

        Args:
            employer_data: Данные работодателя

        Returns:
            Название работодателя
        """
        return employer_data.get("name", "")

    @staticmethod
    def get_employer_url(employer_data: Dict[str, Any]) -> str:
        """Извлечение URL работодателя из данных.

        Args:
            employer_data: Данные работодателя

        Returns:
            URL работодателя
        """
        return employer_data.get("alternate_url", "")

    @staticmethod
    def get_vacancy_name(vacancy_data: Dict[str, Any]) -> str:
        """Извлечение названия вакансии из данных.

        Args:
            vacancy_data: Данные вакансии

        Returns:
            Название вакансии
        """
        return vacancy_data.get("name", "")

    @staticmethod
    def get_vacancy_salary(vacancy_data: Dict[str, Any]) -> Optional[int]:
        """Извлечение зарплаты из данных вакансии.

        Args:
            vacancy_data: Данные вакансии

        Returns:
            Зарплата в рублях или None
        """
        salary = vacancy_data.get("salary")
        if salary and salary.get("currency") == "RUR":
            salary_from = salary.get("from")
            salary_to = salary.get("to")
            if salary_from and salary_to:
                return (salary_from + salary_to) // 2
            return salary_from or salary_to
        return None

    @staticmethod
    def get_vacancy_url(vacancy_data: Dict[str, Any]) -> str:
        """Извлечение URL вакансии из данных.

        Args:
            vacancy_data: Данные вакансии

        Returns:
            URL вакансии
        """
        return vacancy_data.get("alternate_url", "")

    @staticmethod
    def get_vacancy_description(vacancy_data: Dict[str, Any]) -> str:
        """Извлечение описания вакансии из данных.

        Args:
            vacancy_data: Данные вакансии

        Returns:
            Описание вакансии
        """
        return vacancy_data.get("description", "")[:1000] if vacancy_data.get("description") else ""