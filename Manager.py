from database import Database

class Manager:
    def init(self, name, phone_number):
        super().__init__(name, phone_number)

    @staticmethod
    def add_manager(db):
        name = input("Введіть ім'я менеджера: ")
        phone_number = input("Введіть номер телефона менеджера: ")

        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("INSERT INTO persons (name, phone_number, type) VALUES (?, ?, ?)",
                           (name, phone_number, "Менеджер"))
            con.commit()

    @staticmethod
    def delete_manager(db):
        managers = Manager.list_managers(db)
        if not managers:
            print("Немає доступних менеджерів для видалення.")
            return

        manager_id_to_delete = input("Введите ID менеджера для удаления: ")

        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM persons WHERE id = ?", (manager_id_to_delete,))
            con.commit()

    @staticmethod
    def list_managers(db, client_type='Менеджер'):
        with db.connection as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM persons WHERE type = ?", (client_type,))
            managers = cursor.fetchall()

        if not managers:
            print("Менеджери відсутні")
            return managers

        return managers
