from database import Database


class Client:
    def __init__(self, name, phone_number):
        super().__init__(name, phone_number)

    @staticmethod
    def add_client(db):
        name = input("Введіть ім'я клієнта: ")
        phone_number = input("Введіть номер телефону клієнта: ")

        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO persons (name, phone_number, type) VALUES (?, ?, ?)",
                           (name, phone_number, "Клієнт"))
            con.commit()

    @staticmethod
    def delete_client(db):
        clients = Client.list_clients(db)
        if not clients:
            print("Немає доступних клієнтів для видалення.")
            return

        client_id_to_delete = input("Введіть ID клієнта для видалення: ")

        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM persons WHERE id = ?", (client_id_to_delete,))
            con.commit()

    @staticmethod
    def list_clients(db, client_type="Клієнт"):
        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM persons WHERE type = ?", (client_type,))
            clients = cursor.fetchall()

        return clients
