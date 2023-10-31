from config import config
import psycopg2
from db_manager import DBManager
from hh_api import HeadHunterAPI
from db_creator import DBCreator

COMMANDS_FOR_PRINT = """
0 - Выход из программы.

1 - Cписок всех вакансий.

2 - Cписок компаний и количество вакансий в каждой из них.

3 - Cредняя заработная плата.

4 - Список вакансий с зарплатой выше средней.

5 - Список вакансий с указанным ключевым словам.
"""


def main():
    """Пользовательская функция."""
    dbname = 'vacancies'
    params = config()

    DBCreator.create_database(params, dbname)

    params.update({'dbname': dbname})

    with psycopg2.connect(**params) as conn:
        with conn.cursor() as cur:
            DBCreator.create_companies_table(cur)
            DBCreator.create_vacancies_table(cur)
            companies = HeadHunterAPI.get_companies()
            DBCreator.insert_companies_data(cur, companies)
            vacancies = HeadHunterAPI().get_vacancies()
            DBCreator.insert_vacancies_data(cur, vacancies)
            conn.commit()
            print("Привет! Я программа для твоего удобного поиска работы.\nВот мой список команд:")

            while True:
                command = input(f"{COMMANDS_FOR_PRINT}\nНапиши номер команды: ")
                if command == "1":
                    for i in DBManager.get_all_vacancies(cur):
                        print(f"Вакансия: - {i[0]}\n"
                              f"Зарплата: {i[1]} - {i[2]}\n"
                              f"Город: {i[3]}, Компания - {i[4]}\n"
                              f"{'_' * 10}")

                elif command == "2":
                    for i in DBManager.get_companies_and_vacancies_count(cur):
                        print(f"Компания - {i[0]}, Количество вакансий:{i[1]}\n"
                              f"{'_' * 10}")

                elif command == "3":
                    for i in DBManager.get_avg_salary(cur):
                        print(f"Средняя зарплата - {round(i[0])}\n"
                              f"{'_' * 10}")

                elif command == "4":
                    for i in DBManager.get_vacancies_with_highest_salary(cur):
                        print(f"Вакансия - {i[0]}\n"
                              f"Зарплата: {i[1]} - {i[2]}\n"
                              f"Компания - {i[3]}\n"
                              f"{'_' * 10}")

                elif command == "5":
                    for i in DBManager.get_vacancies_with_keyword(cur, input("Введите ключевое слово: ")):
                        print(f"Вакансия - {i[0]}\n"
                              f"Зарплата: {i[1]} - {i[2]}\n"
                              f"Компания - {i[3]}\n"
                              f"{'_' * 10}")

                elif command == "0":
                    print("Удачного собеседования! Пока!")
                    exit(0)
                else:
                    print("Нет такой команды. Попробуйте еще.")


if __name__ == '__main__':
    main()
