import psycopg2


class DBCreator:
    """Класс для создания БД и заполнения их данными."""
    @staticmethod
    def create_database(params: dict, dbname: str):
        """Создания новой базы данных."""
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {dbname}")  # Проверяем существует ли БД с таким именем.
        cur.execute(f"CREATE DATABASE {dbname}")  # Создаем свою БД.

        cur.close()
        conn.close()

    @staticmethod
    def create_vacancies_table(cur):
        """Создаем таблицы с вакансиями."""
        cur.execute("CREATE TABLE IF NOT EXISTS vacancies ("
                    "vacancy_id SERIAL PRIMARY KEY,"
                    "name VARCHAR(100) NOT NULL,"
                    "salary_min INT,"
                    "salary_max INT,"
                    "salary_currency VARCHAR(10),"
                    "city VARCHAR(50) NOT NULL,"
                    "company_id INT REFERENCES companies(company_id))")

    @staticmethod
    def insert_vacancies_data(cur, vacancies: list[dict]):
        """Метод для заполнения нашу таблицу вакансиями."""
        for vacancy in vacancies:
            if vacancy['salary'] is None:
                cur.execute("INSERT INTO vacancies (name, salary_min, salary_max, salary_currency, city, company_id)"
                            "VALUES (%s, %s, %s, %s, %s, %s)", (vacancy['name'],
                                                                0,
                                                                0,
                                                                "null",
                                                                vacancy['area']['name'],
                                                                vacancy['employer']['id']))
            else:
                cur.execute("INSERT INTO vacancies (name, salary_min, salary_max, salary_currency, city, company_id)"
                            "VALUES (%s, %s, %s, %s, %s, %s)", (vacancy['name'],
                                                                vacancy['salary']['from'] if vacancy['salary'][
                                                                                                 'from'] is not None else 0,
                                                                vacancy['salary']['to'] if vacancy['salary'][
                                                                                               'to'] is not None else 0,
                                                                vacancy['salary']['currency'] if vacancy['salary'][
                                                                                                     'currency'] is not None else "null",
                                                                vacancy['area']['name'],
                                                                vacancy['employer']['id']))

    @staticmethod
    def create_companies_table(cur):
        """Метод для создания таблицы с компаниями."""
        cur.execute("CREATE TABLE IF NOT EXISTS companies ("
                    "company_id INT PRIMARY KEY,"
                    "company_name VARCHAR(100),"
                    "company_url VARCHAR(200))")

    @staticmethod
    def insert_companies_data(cur, companies: list[dict]):
        """Метод для заполнения нашу таблицу компаниями."""
        for company in companies:
            cur.execute("INSERT INTO companies (company_id ,company_name, company_url) "
                        "VALUES (%s, %s, %s)", (company['id'], company['name'], company['alternate_url']))
