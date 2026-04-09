import pytest
from pathlib import Path
from hh_parser.core.parser import Vacancy
from hh_parser.exporter.csv_exporter import CSVExporter


@pytest.fixture
def sample_vacancies():
    """Пример списка вакансий."""
    return [
        Vacancy(
            id="1",
            name="Python Developer",
            salary="100000",
            employer="TechCorp",
            link="https://hh.ru/vacancy/1",
            description="Great job",
            requirements="Python",
            experience="3 года"
        )
    ]


class TestCSVExporter:
    """Тесты для CSVExporter."""

    def test_export_empty_list(self, sample_vacancies):
        """Тест экспорта пустого списка."""
        exporter = CSVExporter("test.csv")
        with pytest.raises(ValueError):
            exporter.export([])

    def test_export_success(self, sample_vacancies, tmp_path):
        """Тест успешного экспорта."""
        filename = tmp_path / "test.csv"
        exporter = CSVExporter(str(filename))
        result = exporter.export(sample_vacancies)

        assert result.exists()
        with open(result, encoding='utf-8') as f:
            content = f.read()
            assert "Python Developer" in content