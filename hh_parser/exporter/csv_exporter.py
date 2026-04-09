"""
Модуль для экспорта вакансий в CSV формат.
"""
import csv
from typing import List
from pathlib import Path
from ..core.parser import Vacancy


class CSVExporter:
    """
    Класс для экспорта вакансий в CSV файл.
    """

    def __init__(self, filename: str = "vacancies.csv"):
        """
        Инициализация экспортера.

        Args:
            filename (str): Имя выходного CSV файла
        """
        self.filename = filename

    def export(self, vacancies: List[Vacancy]) -> Path:
        """
        Экспорт списка вакансий в CSV файл.

        Args:
            vacancies (List[Vacancy]): Список вакансий для экспорта

        Returns:
            Path: Путь к созданному файлу

        Raises:
            ValueError: Если список вакансий пустой
        """
        if not vacancies:
            raise ValueError("Список вакансий пустой")

        filepath = Path(self.filename)
        fieldnames = [
            'id', 'name', 'salary', 'employer', 'link',
            'description', 'requirements', 'experience'
        ]

        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for vacancy in vacancies:
                writer.writerow({
                    'id': vacancy.id,
                    'name': vacancy.name,
                    'salary': vacancy.salary or '',
                    'employer': vacancy.employer,
                    'link': vacancy.link,
                    'description': vacancy.description,
                    'requirements': vacancy.requirements,
                    'experience': vacancy.experience
                })

        return filepath