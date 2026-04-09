#!/usr/bin/env python3
"""
Запуск проекта hh-parser.
"""
import argparse
from hh_parser.database.sqlite_db import SQLiteDBManager


def main():
    parser = argparse.ArgumentParser(description='HH Vacancies Manager')
    parser.add_argument('--fill', action='store_true', help='Заполнить данными')
    parser.add_argument('--show', choices=['companies', 'vacancies', 'avg', 'higher', 'keyword'],
                        help='Что показать')
    parser.add_argument('--keyword', help='Ключевое слово')
    args = parser.parse_args()

    db = SQLiteDBManager()

    if args.fill:
        db.fill_test_data()
        print("✅ Данные заполнены!")
        return

    print("\n" + "=" * 50)

    if args.show == 'companies':
        print("🏢 КОМПАНИИ И ВАКАНСИИ:")
        for name, count in db.get_companies_and_vacancies_count():
            print(f"  {name:<20} | {count:>3} вакансий")

    elif args.show == 'vacancies':
        print("📋 ВСЕ ВАКАНСИИ:")
        for vac in db.get_all_vacancies()[:10]:
            salary = f"{vac['salary']:,.0f}₽" if vac['salary'] else "Не указана"
            print(f"  {vac['company']:<15} | {vac['name']:<30} | {salary}")

    elif args.show == 'avg':
        avg = db.get_avg_salary()
        print(f"💰 СРЕДНЯЯ ЗАРПЛАТА: {avg:,.0f}₽" if avg else "Нет данных")

    elif args.show == 'higher':
        print("🔥 ВЫШЕ СРЕДНЕЙ:")
        for vac in db.get_vacancies_with_higher_salary()[:5]:
            print(f"  {vac['company']:<15} | {vac['name']:<30} | {vac['salary']:,.0f}₽")

    elif args.show == 'keyword' and args.keyword:
        print(f"🔍 ПО '{args.keyword.upper()}':")
        for vac in db.get_vacancies_with_keyword(args.keyword)[:5]:
            print(f"  {vac['company']:<15} | {vac['name']}")

    print("=" * 50)


if __name__ == "__main__":
    main()