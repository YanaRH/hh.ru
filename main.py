from hh_parser.database.sqlite_db import SQLiteDBManager


def main():
    db = SQLiteDBManager()

    parser = argparse.ArgumentParser()
    parser.add_argument('--fill', action='store_true')
    parser.add_argument('--show', choices=['companies', 'vacancies', 'avg', 'higher', 'keyword'])
    parser.add_argument('--keyword')
    args = parser.parse_args()

    if args.fill:
        db.fill_test_data()
        return

    if args.show == 'companies':
        print("🏢 Компании:")
        for name, count in db.get_companies_and_vacancies_count():
            print(f"  {name}: {count}")

    # ... остальные команды