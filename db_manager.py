class DBManager:
    """Класс для работы с базой данных."""

    @staticmethod
    def get_all_vacancies(cur):
        """Метод получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        script = """SELECT name, salary_min, salary_max, city, companies.company_name FROM vacancies
        JOIN companies ON companies.company_id = vacancies.company_id"""

        cur.execute(script)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_companies_and_vacancies_count(cur):
        """Метод для получения компаний и количества вакансий у каждой компании."""
        script = """SELECT company_name, COUNT(*) FROM companies
        JOIN vacancies ON companies.company_id = vacancies.company_id
        GROUP BY company_name"""

        cur.execute(script)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_avg_salary(cur):
        """Метод получает среднюю зарплату по вакансиям."""
        query = """
                SELECT AVG((salary_min + salary_max) / 2)
                FROM vacancies"""
        cur.execute(query)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_vacancies_with_highest_salary(cur):
        """Метод для получения всех вакансий, у которых зарплата выше средней."""
        script = """SELECT name, salary_min, salary_max, companies.company_name FROM vacancies
                    LEFT JOIN companies ON vacancies.company_id = companies.company_id
                    WHERE salary_max > (SELECT AVG((salary_min + salary_max) / 2) FROM vacancies)"""

        cur.execute(script)
        result = cur.fetchall()
        return result

    @staticmethod
    def get_vacancies_with_keyword(cur, keyword):
        """Получаем список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        script = f"""SELECT name, salary_min, salary_max, companies.company_name FROM vacancies
        JOIN companies ON vacancies.company_id = companies.company_id
        WHERE name LIKE '%{keyword}%'"""

        cur.execute(script)
        result = cur.fetchall()
        return result
