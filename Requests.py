from database import Database
import datetime


def count_trading_points(db):
    with db.connection as con:
        cursor = con.cursor()
        cursor.execute("SELECT COUNT(*) FROM contracts")
        count = cursor.fetchone()[0]

        print(" ")
        print("Кількість торгових точок")
        print(count)
        print(" ")


def list_trading_point_types(db):
    with db.connection as con:
        cursor = con.cursor()
        cursor.execute("SELECT DISTINCT product_type FROM contracts")
        product_types = cursor.fetchall()

        product_types = [item[0] for item in product_types]

        print(" ")
        print("Список типів торгових точок")
        print(', '.join(product_types))
        print(" ")


def longest_contract(db):
    with db.connection as con:
        cursor = con.cursor()
        cursor.execute("SELECT foodMarket_name, start_data, end_data FROM contracts ORDER BY (end_data - start_data) "
                       "DESC LIMIT 1")
        longest_contracts = cursor.fetchone()

        if longest_contracts:
            contract_name, start_date_str, end_date_str = longest_contracts
            start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y').timestamp()
            end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').timestamp()

            term_in_months = (datetime.datetime.fromtimestamp(end_date) - datetime.datetime.fromtimestamp(
                start_date)).days // 30

            print(" ")
            print("Найдовший контракт")
            print("Назва:", contract_name)
            print("Початкова дата:", datetime.datetime.fromtimestamp(start_date).strftime('%Y-%m-%d'))
            print("Кінцева дата:", datetime.datetime.fromtimestamp(end_date).strftime('%Y-%m-%d'))
            print("Термін в місяцях:", term_in_months)
            print(" ")
        else:
            print("No contracts found.")


def most_expensive_contract(db):
    with db.connection as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM contracts ORDER BY cost DESC LIMIT 1")
        most_expensive_contracts = cursor.fetchone()
        if most_expensive_contracts:
            contract_id, foodMarket_name, product_type, point_number, start_data, end_data, cost, client_id, \
                manager_id = most_expensive_contracts
            print(" ")
            print("Найдорожчий контракт")
            print(f"Назва: {foodMarket_name}\n"
                  f"Вартість: {cost}")
            print(" ")
        else:
            print("No contracts found.")


def calculate_average_rental_term(db):
    with db.connection as con:
        cursor = con.cursor()
        cursor.execute("SELECT start_data, end_data FROM contracts")
        all_contracts = cursor.fetchall()

        if not all_contracts:
            print("No contracts found.")
            return

        total_term_in_months = 0
        for start_date_str, end_date_str in all_contracts:
            start_date = datetime.datetime.strptime(start_date_str, '%d.%m.%Y').timestamp()
            end_date = datetime.datetime.strptime(end_date_str, '%d.%m.%Y').timestamp()

            term_in_months = (datetime.datetime.fromtimestamp(end_date) - datetime.datetime.fromtimestamp(
                start_date)).days // 30

            total_term_in_months += term_in_months

        average_rental_term = total_term_in_months / len(all_contracts)
        print(" ")
        print("Середній термін оренди всіх контрактів в місяцях:", average_rental_term)
        print(" ")
