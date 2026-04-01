#!/usr/bin/env python3
"""
HH.ru парсер вакансий
✅ SQLite версия - БЕЗ PostgreSQL!
"""

import os
from dotenv import load_dotenv
from typing import Optional

# Импорты
from src.hh_api import HHApi
from src.database import Database
from src.db_manager import DBManager

# Компании для парсинга
EMPLOYER_IDS = [
    "1740", "3529", "3776", "84585", "15478",  # Топ компании
    "78638", "232402", "4181", "501", "153"
]


def load_dotenv_vars():
    """Загрузка .env"""
    load_dotenv(encoding='utf-8')


def create_database_and_tables():
    """✅ Создание SQLite БД"""
    print("🚀 Создание SQLite БД...")
    db = Database()
    print("✅ hh_parser.db готова!")
    return db


def load_data_from_hh(db: Database):
    """📊 Загрузка данных HH.ru"""
    print("\n🌐 Загрузка данных с HH.ru...")

    hh_api = HHApi()
    db.clear_all_data()

    total_vacancies = 0
    for employer_id in EMPLOYER_IDS:
        print(f"\n📊 Компания {employer_id}...")

        # Данные компании
        employer_data = hh_api.get_employer(employer_id)
        company_name = hh_api.get_employer_name(employer_data)
        company_url = hh_api.get_employer_url(employer_data)
        company_description = employer_data.get("description", "")[:500]

        # Сохранение компании
        company_id = db.insert_company(
            employer_id, company_name, company_url, company_description
        )
        print(f"  ✅ {company_name}")

        # Вакансии
        vacancies = hh_api.get_all_vacancies(employer_id)
        print(f"  📈 {len(vacancies)} вакансий")

        for vacancy in vacancies[:10]:  # Лимит 10 на компанию для теста
            db.insert_vacancy(
                vacancy.get("id", ""),
                company_id,
                hh_api.get_vacancy_name(vacancy),
                hh_api.get_vacancy_salary(vacancy),
                hh_api.get_vacancy_url(vacancy),
                hh_api.get_vacancy_description(vacancy)
            )

        total_vacancies += len(vacancies)

    print(f"\n🎉 Загружено {total_vacancies} вакансий!")
    return total_vacancies


def user_interface(db_manager: DBManager):
    """🎮 Интерфейс пользователя"""
    while True:
        print("\n" + "=" * 60)
        print("📊 МЕНЮ АНАЛИЗА ВАКАНСИЙ:")
        print("1. 🏢 Компании и количество вакансий")
        print("2. 📋 Все вакансии")
        print("3. 💰 Средняя зарплата")
        print("4. ⭐ Вакансии выше средней")
        print("5. 🔍 Поиск по ключевому слову")
        print("0. ❌ Выход")
        print("=" * 60)

        choice = input("Выберите (0-5): ").strip()

        if choice == "1":
            results = db_manager.get_companies_and_vacancies_count()
            print("\n🏢 КОМПАНИИ:")
            for item in results:
                print(f"  {item['company']:<30} | {item['vacancies_count']:>4} вакансий")

        elif choice == "2":
            results = db_manager.get_all_vacancies()
            print(f"\n📋 ВСЕ ВАКАНСИИ ({len(results)}):")
            for item in results[:20]:  # Первые 20
                salary = f"{item['salary']:,} ₽" if item['salary'] else "Не указана"
                print(f"  {item['company']:<25} | {item['vacancy']:<40} | {salary}")

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"\n💰 СРЕДНЯЯ ЗАРПЛАТА: {avg_salary:,.0f} ₽")

        elif choice == "4":
            results = db_manager.get_vacancies_with_higher_salary()
            print(f"\n⭐ ПРЕМИУМ ВАКАНСИИ ({len(results)}):")
            for item in results:
                print(f"  {item['company']:<25} | {item['vacancy']:<35} | {item['salary']:>8,} ₽")

        elif choice == "5":
            keyword = input("\n🔍 Ключевое слово: ").strip().lower()
            results = db_manager.get_vacancies_with_keyword(keyword)
            print(f"\n📈 Найдено: {len(results)} вакансий")
            for item in results:
                salary = f"{item['salary']:,} ₽" if item['salary'] else "Не указана"
                print(f"  {item['company']:<25} | {item['vacancy']}")

        elif choice == "0":
            print("\n👋 До свидания!")
            break
        else:
            print("❌ Неверный выбор!")


def main():
    """🎯 Главная функция"""
    print("🤖 HH.ru ВАКАНСИИ ПАРСЕР (SQLite)")
    print("=" * 50)

    # 1. Настройка
    load_dotenv_vars()

    # 2. БД
    db = create_database_and_tables()

    # 3. Парсинг
    total = load_data_from_hh(db)

    # 4. UI
    db_manager = DBManager(db_path="hh_parser.db")
    user_interface(db_manager)

    # 5. Закрытие
    db.close()
    print("\n✅ Работа завершена!")


if __name__ == "__main__":
    main()