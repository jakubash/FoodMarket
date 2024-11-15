from database import Database

class Contract:
    def __init__(self, foodMarket_name, product_type, point_number, start_data, end_data, cost):
        super().__init__(foodMarket_name, product_type, point_number, start_data, end_data, cost)

    @staticmethod
    def add_contract(db):
        # Вибір клієнта
        print("Доступні клієнти:")
        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM persons WHERE type = 'Клієнт'")
            clients = cursor.fetchall()
            for client in clients:
                print(f"ID: {client[0]}, Ім'я: {client[1]}")

        if not clients:
            print("Немає доступних клієнтів. Додайте клієнта перед створенням контракту.")
            return

        client_id = input("Введіть ID клієнта: ")

        # Вибір менеджера
        print("Доступні менеджери:")
        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM persons WHERE type = 'Менеджер'")
            managers = cursor.fetchall()
            for manager in managers:
                print(f"ID: {manager[0]}, Ім'я: {manager[1]}")

        if not managers:
            print("Немає доступних менеджерів. Додайте менеджера перед створенням контракту.")
            return

        manager_id = input("Введіть ID менеджера: ")

        # Запит користувача залишається без змін
        foodMarket_name = input("Введіть назву магазину: ")
        product_type = input("Введіть тип продукту: ")
        point_number = input("Введіть номер точки: ")
        start_data = input("Введіть початкову дату: ")
        end_data = input("Введіть кінцеву дату: ")
        cost = input("Введіть вартість: ")

        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO contracts (foodMarket_name, product_type, point_number, start_data, end_data, "
                           "cost, client_id, manager_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                           (foodMarket_name, product_type, point_number, start_data, end_data, cost, client_id,
                            manager_id))
            con.commit()

    @staticmethod
    def delete_contract(db):
        contracts = Contract.list_contracts(db)
        if not contracts:
            print("Контракти відсутні.")
            return

        print("Доступні контракти:")
        for contract in contracts:
            print(f"ID: {contract[0]}, Магазин: {contract[1]}")

        contract_id_to_delete = input("Введіть ID контракта для видалення: ")

        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM contracts WHERE id = ?", (contract_id_to_delete,))
            con.commit()

    @staticmethod
    def list_contracts(db):
        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM contracts")
            contracts = cursor.fetchall()

        return contracts

    @staticmethod
    def get_contract_details(db, contract_id):
        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM contracts WHERE id = ?", (contract_id,))
            contract = cursor.fetchone()

        if not contract:
            return None
        else:
            return contract
