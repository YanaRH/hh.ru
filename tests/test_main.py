"""Тесты для hh_parser."""
import pytest
import sqlite3
from main import SQLiteDBManager, fetch_hh_data, parse_vacancy


def test_db_init():
    """Тест создания БД."""
    db = SQLiteDBManager("test.db")
    cursor = db.conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vacancies'")
    assert cursor.fetchone() is not None


def test_add_vacancy():
    """Тест добавления вакансии."""
    db = SQLiteDBManager("test.db")
    vacancy = {
        'id': 'test123', 'name': 'Test Job', 'company': 'Test Corp',
        'salary_from': 100000, 'salary_to': 200000, 'currency': 'RUR',
        'url': 'https://test.ru', 'area': 'Test City'
    }
    db.add_vacancy(vacancy)

    cursor = db.conn.cursor()
    cursor.execute("SELECT * FROM vacancies WHERE id='test123'")
    result = cursor.fetchone()
    assert result['company'] == 'Test Corp'


def test_companies_count():
    """Тест статистики компаний."""
    db = SQLiteDBManager("test.db")
    assert isinstance(db.get_companies_and_vacancies_count(), list)


def test_parse_vacancy():
    """Тест парсинга вакансии."""
    vacancy = {
        'id': '1', 'name': 'Python Dev', 'employer': {'name': 'Yandex'},
        'salary': {'from': 200000, 'to': None, 'currency': 'RUR'},
        'alternate_url': 'https://hh.ru/1', 'area': {'name': 'Москва'}
    }
    parsed = parse_vacancy(vacancy)
    assert parsed['company'] == 'Yandex'
    assert parsed['salary_from'] == 200000