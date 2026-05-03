#!/usr/bin/env python3
"""
Парсер вакансий hh.ru через официальный API.
"""
import argparse
import requests
import sqlite3
from typing import List, Dict, Any, Tuple


class SQLiteDBManager:
    """Менеджер SQLite базы данных для вакансий hh.ru."""

    def __init__(self, db_path: str = "hh_vacancies.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self) -> None:
        """Создает таблицу vacancies."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                company TEXT NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                currency TEXT,
                url TEXT,
                area TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """Добавляет вакансию в БД."""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO vacancies 
            (id, name, company, salary_from, salary_to, currency, url, area)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vacancy_data['id'], vacancy_data['name'], vacancy_data['company'],
            vacancy_data['salary_from'], vacancy_data['salary_to'],
            vacancy_data['currency'], vacancy_data['url'], vacancy_data['area']
        ))
        self.conn.commit()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Статистика компаний."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT company, COUNT(*) as count 
            FROM vacancies GROUP BY company ORDER BY count DESC
        ''')
        return cursor.fetchall()


def fetch_hh_data(pages: int = 1) -> List[Dict[str, Any]]:
    """Загрузка с API hh.ru."""
    url = 'https://api.hh.ru/vacancies'
    vacancies = []
    for page in range(pages):
        print(f"📄 {page+1}/{pages}")
        params = {'area': 1, 'page': page, 'per_page': 100, 'only_with_salary': True}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        vacancies.extend(data['items'])
    print(f"📥 {len(vacancies)} вакансий")
    return vacancies


def parse_vacancy(vacancy: Dict[str, Any]) -> Dict[str, Any]:
    """Парсинг JSON вакансии."""
    salary = vacancy.get('salary', {})
    return {
        'id': vacancy['id'],
        'name': vacancy['name'],
        'company': vacancy['employer']['name'],
        'salary_from': salary.get('from'),
        'salary_to': salary.get('to'),
        'currency': salary.get('currency'),
        'url': vacancy['alternate_url'],
        'area': vacancy['area']['name']
    }


def main() -> None:
    """CLI интерфейс."""
    db = SQLiteDBManager()
    parser = argparse.ArgumentParser(description='hh.ru парсер')
    parser.add_argument('--fill', action='store_true')
    parser.add_argument('--fill-hh', action='store_true')
    parser.add_argument('--show', choices=['companies'])
    parser.add_argument('--pages', type=int, default=1)
    args = parser.parse_args()

    if args.fill:
        test_data = [
            {'id': '1', 'name': 'Python', 'company': 'Yandex', 'salary_from': 200000, 'salary_to': None, 'currency': 'RUR', 'url': 'test', 'area': 'Москва'},
            {'id': '2', 'name': 'Python', 'company': 'Yandex', 'salary_from': 180000, 'salary_to': 250000, 'currency': 'RUR', 'url': 'test', 'area': 'Москва'},
        ]
        for data in test_data:
            db.add_vacancy(data)
        print("✅ Тестовые данные!")
        return

    if args.fill_hh:
        vacancies = fetch_hh_data(args.pages)
        saved = sum(1 for _ in map(db.add_vacancy, map(parse_vacancy, vacancies)))
        print(f"✅ {saved} вакансий!")
        return

    if args.show == 'companies':
        print("\n🏢 Компании:")
        for name, count in db.get_companies_and_vacancies_count()[:10]:
            print(f"  {name:<30} {count:>3d}")
    else:
        print("👉 --fill | --fill-hh --pages 2 | --show companies")


if __name__ == "__main__":
    main()