import sqlite3
import os
from typing import Optional


class Database:
    def __init__(self, db_path="hh_parser.db"):
        self.db_path = db_path
        self.conn = None
        self.create_tables()

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn

    def create_tables(self):
        """Создание таблиц SQLite"""
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hh_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                url TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                hh_id TEXT UNIQUE NOT NULL,
                company_id INTEGER,
                name TEXT NOT NULL,
                salary INTEGER,
                url TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
        """)

        conn.commit()
        cursor.close()
        print("✅ SQLite БД готова (файл: hh_parser.db)")

    def insert_company(self, hh_id: str, name: str, url: str, description: str = "") -> int:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO companies (hh_id, name, url, description)
            VALUES (?, ?, ?, ?)
        """, (hh_id, name, url, description))
        company_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        return company_id

    def insert_vacancy(self, hh_id: str, company_id: int, name: str,
                       salary: Optional[int], url: str, description: str = "") -> int:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO vacancies (hh_id, company_id, name, salary, url, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (hh_id, company_id, name, salary, url, description))
        vacancy_id = cursor.lastrowid
        conn.commit()
        cursor.close()
        return vacancy_id

    def get_company_id_by_hh_id(self, hh_id: str) -> Optional[int]:
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM companies WHERE hh_id = ?", (hh_id,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def clear_all_data(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vacancies")
        cursor.execute("DELETE FROM companies")
        conn.commit()
        cursor.close()
        print("✅ Данные очищены")

    def close(self):
        if self.conn:
            self.conn.close()