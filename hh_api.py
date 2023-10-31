import requests
from abc import ABC, abstractmethod

COMPANIES = {"yandex": "1740",
             "teremok": "27879",
             "abcp": "561525",
             "simplex": "1250899",
             "writers_way": "2175093",
             "tolyati": "9139449",
             "ozon": "2180",
             "fix_price": "196621",
             "start_job": "4811615"}


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def __init__(self):
        """Инициализируем наш класс."""
        pass

    @abstractmethod
    def get_vacancies(self):
        """Метод для получения списка вакансий по API."""
        pass


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с HeadHunter."""

    def __init__(self):
        self.api_url = "https://api.hh.ru/vacancies?employer_id="
        self.params = {
            "pages": 0,
            "per_page": 100,
            "only_with_vacancies": True
        }

    def get_vacancies(self):
        """Метод для получения списка вакансий по API."""
        vacancies = []
        for company in COMPANIES.values():
            response = requests.get(f"{self.api_url}{company}", params=self.params)
            data = response.json()['items']
            vacancies.extend(data)
            self.params["pages"] += 1
        return vacancies

    @staticmethod
    def get_companies():
        """Метод для получения списка компаний по API."""
        companies = []
        for company in COMPANIES.values():
            response = requests.get(f"https://api.hh.ru/employers/{company}").json()
            companies.append(response)
        return companies
