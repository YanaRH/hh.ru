"""
Главная точка входа в приложение.
"""
import argparse
import logging
from pathlib import Path
from hh_parser.core.parser import HHParser  # ← ИСПРАВЛЕННЫЙ ИМПОРТ
from hh_parser.exporter.csv_exporter import CSVExporter  # ← ИСПРАВЛЕННЫЙ ИМПОРТ


def setup_logging():
    """Настройка логирования для приложения."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main():
    """Основная функция приложения."""
    parser_arg = argparse.ArgumentParser(description='Парсер вакансий HeadHunter')
    parser_arg.add_argument('query', help='Поисковый запрос')
    parser_arg.add_argument('--pages', type=int, default=1, help='Количество страниц')
    parser_arg.add_argument('--output', default='vacancies.csv', help='Имя выходного файла')

    args = parser_arg.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info(f"Парсинг вакансий: {args.query}")

    hh_parser = HHParser(args.query)
    all_vacancies = []

    for page in range(args.pages):
        vacancies = hh_parser.search_vacancies(page=page)
        all_vacancies.extend(vacancies)

    logger.info(f"Найдено вакансий: {len(all_vacancies)}")

    exporter = CSVExporter(args.output)
    output_file = exporter.export(all_vacancies)

    logger.info(f"Экспорт завершен: {output_file}")


if __name__ == "__main__":
    main()