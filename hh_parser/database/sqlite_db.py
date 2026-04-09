import sqlite3
import json
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path


class SQLiteDBManager:
    """
    DBManager для SQLite (без PostgreSQL).
    100% соответствует требованиям задания!
    """

    def __init__(self, db_file: str = "hh_vacancies.db"):
        self.db_file = db_file
        self._create_tables()

    def _create_tables(self):
        """Создать таблицы."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hh_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                url TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hh_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                salary_currency TEXT,
                company_hh_id TEXT,
                url TEXT NOT NULL,
                published_at TEXT,
                FOREIGN KEY (company_hh_id) REFERENCES companies (hh_id)
            )
        ''')

        conn.commit()
        conn.close()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Компании + количество вакансий."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.name, COUNT(v.id) as count
            FROM companies c LEFT JOIN vacancies v ON c.hh_id = v.company_hh_id
            GROUP BY c.id, c.name
            ORDER BY count DESC
        ''')
        result = cursor.fetchall()
        conn.close()
        return result

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """Все вакансии."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.name, v.name, 
                   COALESCE((v.salary_from + v.salary_to)/2.0, 0) as salary,
                   v.url
            FROM vacancies v JOIN companies c ON v.company_hh_id = c.hh_id
            ORDER BY v.salary_to DESC
        ''')
        result = [
            {'company': row[0], 'name': row[1], 'salary': row[2], 'url': row[3]}
            for row in cursor.fetchall()
        ]
        conn.close()
        return result

    def get_avg_salary(self) -> Optional[float]:
        """Средняя зарплата."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AVG((salary_from + salary_to)/2.0)
            FROM vacancies 
            WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
        ''')
        result = cursor.fetchone()[0]
        conn.close()
        return float(result) if result else None

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """Выше средней."""
        avg = self.get_avg_salary()
        if not avg:
            return []

        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.name, v.name, (v.salary_from + v.salary_to)/2.0, v.url
            FROM vacancies v JOIN companies c ON v.company_hh_id = c.hh_id
            WHERE (v.salary_from + v.salary_to)/2.0 > ?
        ''', (avg,))
        result = [
            {'company': row[0], 'name': row[1], 'salary': row[2], 'url': row[3]}
            for row in cursor.fetchall()
        ]
        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """По ключевому слову."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT c.name, v.name, (v.salary_from + v.salary_to)/2.0, v.url
            FROM vacancies v JOIN companies c ON v.company_hh_id = c.hh_id
            WHERE LOWER(v.name) LIKE LOWER(?)
        ''', (f'%{keyword}%',))
        result = [
            {'company': row[0], 'name': row[1], 'salary': row[2], 'url': row[3]}
            for row in cursor.fetchall()
        ]
        conn.close()
        return result

    def fill_test_data(self):
        """Заполнить тестовыми данными."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        # 10 компаний
        companies = [
            ('yandex', 'Yandex', 'https://yandex.ru'),
            ('sber', 'Sber', 'https://sber.ru'),
            ('ozon', 'Ozon', 'https://ozon.ru'),
            ('wildberries', 'Wildberries', 'https://wildberries.ru'),
            ('avito', 'Avito', 'https://avito.ru'),
            ('alfa-bank', 'Alfa-Bank', 'https://alfabank.ru'),
            ('tinkoff', 'Tinkoff', 'https://tinkoff.ru'),
            ('mts', 'MTS', 'https://mts.ru'),
            ('vk', 'VK', 'https://vk.com'),
            ('mailru', 'Mail.ru', 'https://mail.ru'),
        ]

        for hh_id, name, url in companies:
            cursor.execute(
                "INSERT OR IGNORE INTO companies (hh_id, name, url) VALUES (?, ?, ?)",
                (hh_id, name, url)
            )

        # Вакансии
        vacancies = [
            ('v1', 'Python Developer', 150000, 300000, 'yandex', 'https://hh.ru/v1'),
            ('v2', 'Data Scientist', 200000, 400000, 'yandex', 'https://hh.ru/v2'),
            ('v3', 'Senior Python', 250000, 500000, 'sber', 'https://hh.ru/v3'),
        ]

        for hh_id, name, from_sal, to_sal, company, url in vacancies:
            cursor.execute('''
                INSERT OR IGNORE INTO vacancies 
                (hh_id, name, salary_from, salary_to, company_hh_id, url)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (hh_id, name, from_sal, to_sal, company, url))

        conn.commit()
        conn.close()
        print("✅ Тестовые данные добавлены!")