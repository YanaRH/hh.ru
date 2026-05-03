import requests
import time
from typing import List, Dict, Any, Optional


class HHApi:
    """API HeadHunter.ru"""

    BASE_URL = "https://api.hh.ru"
    HEADERS = {
        'User-Agent': 'HHParser/1.0 (Windows; Python 3.12)'
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HHApi.HEADERS)  # ✅ ИСПРАВЛЕНО!

    def get_employer(self, employer_id: str) -> Dict[str, Any]:
        """Данные компании"""
        url = f"{HHApi.BASE_URL}/employers/{employer_id}"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Компания {employer_id}: {e}")
            return {}

    def get_employer_name(self, data: Dict[str, Any]) -> str:
        return data.get('name', 'Неизвестная компания')

    def get_employer_url(self, data: Dict[str, Any]) -> str:
        urls = data.get('alternate_urls', [])
        return urls[0].get('www', '') if urls else ''

    def get_all_vacancies(self, employer_id: str, per_page: int = 100) -> List[Dict]:
        """Все вакансии компании"""
        vacancies = []
        page = 0

        while True:
            url = f"{HHApi.BASE_URL}/vacancies"
            params = {
                'employer_id': employer_id,
                'page': page,
                'per_page': per_page,
                'only_with_salary': 'false'
            }

            try:
                response = self.session.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                new_vacancies = data.get('items', [])
                vacancies.extend(new_vacancies)

                print(f"     📄 Страница {page + 1}: {len(new_vacancies)} вакансий")

                if page >= data.get('pages', 1) - 1 or not new_vacancies:
                    break

                page += 1
                time.sleep(0.5)  # Пауза API

            except Exception as e:
                print(f"     ❌ Страница {page}: {e}")
                break

        return vacancies[:50]  # Лимит 50 вакансий на компанию

    def get_vacancy_name(self, vacancy: Dict) -> str:
        return vacancy.get('name', 'Не указано')

    def get_vacancy_salary(self, vacancy: Dict) -> Optional[int]:
        salary = vacancy.get('salary')
        if not salary:
            return None

        from_salary = salary.get('from') or 0
        to_salary = salary.get('to') or 0

        return (from_salary + to_salary) // 2 if from_salary or to_salary else None

    def get_vacancy_url(self, vacancy: Dict) -> str:
        return vacancy.get('alternate_url', '')

    def get_vacancy_description(self, vacancy: Dict) -> str:
        snippet = vacancy.get('snippet', {})
        return (snippet.get('requirement') or '')[:300]