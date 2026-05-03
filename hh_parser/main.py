#!/usr/bin/env python3
"""
Парсер вакансий hh.ru через официальный API v1.
Сохраняет в SQLite и показывает статистику компаний.
"""

import argparse
import requests
import sqlite3
from typing import List, Tuple


class HhDatabase:
    """Управление SQLite базой вакансий hh.ru."""

    def __init__(self, db_path: str = "hh.db") -> None:
        """
        Инициализация базы данных.

        Args:
            db_path: Путь к SQLite файлу
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self) -> None:
        """Создает таблицу vacancies."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                company TEXT NOT NULL,
                salary INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_vacancy(self, vacancy: dict) -> None:
        """
        Сохраняет вакансию в БД.

        Args:
            vacancy: Данные вакансии от API
        """
        salary = vacancy.get('salary', {}).get('from', 0)
        self.cursor.execute(
            "INSERT OR REPLACE INTO vacancies VALUES (?,?,?,?)",
            (vacancy['id'], vacancy['name'], vacancy['employer']['name'], salary)
        )
        self.conn.commit()

    def get_company_stats(self) -> List[Tuple[str, int, float]]:
        """
        Статистика компаний: название, количество, средняя ЗП.

        Returns:
            Список (компания, кол-во, средняя ЗП)
        """
        self.cursor.execute("""
            SELECT company, COUNT(*), AVG(salary) 
            FROM vacancies 
            GROUP BY company 
            ORDER BY COUNT(*) DESC
        """)
        return self.cursor.fetchall()


def fetch_hh_vacancies(pages: int = 1, area: int = 1) -> list:
    """
    Загружает вакансии с API hh.ru.

    Args:
        pages: Количество страниц (100 вакансий/страница)
        area: Регион (1=Москва)

    Returns:
        Список вакансий
    """
    url = "https://api.hh.ru/vacancies"
    all_vacancies = []

    for page in range(pages):
        print(f"📄 Загрузка страницы {page + 1}/{pages}")
        response = requests.get(url, params={
            'area': area,
            'page': page,
            'per_page': 100,
            'only_with_salary': True
        })
        response.raise_for_status()
        data = response.json()
        all_vacancies.extend(data['items'])

    print(f"📥 Всего вакансий: {len(all_vacancies)}")
    return all_vacancies


def main() -> None:
    """CLI точка входа."""
    db = HhDatabase()

    parser = argparse.ArgumentParser(description="Парсер hh.ru API")
    parser.add_argument('--fill', type=int, default=1,
                        help='загрузить N страниц (по умолчанию 1)')
    parser.add_argument('--show', action='store_true',
                        help='показать статистику компаний')
    args = parser.parse_args()

    if args.fill:
        print("🌐 Загрузка данных с hh.ru...")
        vacancies = fetch_hh_vacancies(args.fill)

        print("💾 Сохранение в БД...")
        for vacancy in vacancies:
            db.add_vacancy(vacancy)

        print(f"✅ Загружено {len(vacancies)} вакансий!")

    elif args.show:
        print("\n🏢 СТАТИСТИКА КОМПАНИЙ")
        print("-" * 60)
        stats = db.get_company_stats()

        for i, (company, count, avg_salary) in enumerate(stats[:15], 1):
            print(f"{i:2d}. {company:<30} | {count:>3} вак. | {avg_salary:>9,.0f} ₽")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()