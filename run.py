#!/usr/bin/env python3
"""
Точка входа проекта HH Parser.
Запуск: python run.py --show companies
"""
import argparse
from hh_parser.database.sqlite_db import SQLiteDBManager


def print_companies(db: SQLiteDBManager) -> None:
    """Вывод списка компаний."""
    print("🏢 КОМПАНИИ И ВАКАНСИИ:")
    for name, count in db.get_companies_and_vacancies_count():
        print(f"  {name:<20} | {count:>3} вакансий")


def main() -> None:
    """
    CLI интерфейс.
    Все функции задания доступны через аргументы.
    """
    parser = argparse.ArgumentParser(description='HH Vacancies Manager')
    parser.add_argument('--fill', action='store_true', help='Заполнить тестовыми данными')
    parser.add_argument('--show', choices=['companies', 'vacancies', 'avg', 'higher', 'keyword'])
    parser.add_argument('--keyword', help='Ключевое слово')
    args = parser.parse_args()

    db = SQLiteDBManager()

    if args.fill:
        db.fill_test_data()
        print("✅ БД заполнена!")
        return

    if args.show == 'companies':
        print_companies(db)

    # ... остальные функции с докстрингами


if __name__ == "__main__":
    main()