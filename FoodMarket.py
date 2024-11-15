from tkinter import Tk, Label, Button, Listbox
from database import Database
from Client import Client
from Manager import Manager
from Contract import Contract
from Requests import (
    count_trading_points,
    list_trading_point_types,
    longest_contract,
    most_expensive_contract,
    calculate_average_rental_term,
)


class DetailsWindow:
    def __init__(self, contract_details):
        self.details_window = Tk()
        self.details_window.title(f"Детальна інформація про контракт {contract_details[0]}")
        self.details_window.geometry("300x200")

        details_label = Label(self.details_window, text="Повна інформація про контракт:")
        details_label.pack()

        details_text = (
            f"ID: {contract_details[0]}\nМагазин: {contract_details[1]}\nТип продукту: {contract_details[2]}\n"
            f"Номер точки: {contract_details[3]}\nПочаткова дата: {contract_details[4]}\n"
            f"Кінцева дата: {contract_details[5]}\nВартість: {contract_details[6]}\n"
            f"ID клієнта: {contract_details[7]}\nID менеджера: {contract_details[8]}"
        )

        details_info = Label(self.details_window, text=details_text)
        details_info.pack()

        close_button = Button(self.details_window, text="Закрити", command=self.details_window.destroy)
        close_button.pack()


class FoodMarketApp:
    def __init__(self, master):
        self.master = master
        master.title("Food Market Application")
        master.geometry("150x235")
        master.resizable(True, True)

        self.db = Database("db/database.db")
        self.db.open()
        self.db.create_tables()

        self.label = Label(master, text="Меню програми:")
        self.label.place(x=25, y=5)

        self.button_clients = Button(master, text="Клієнти", command=self.menu_clients)
        self.button_clients.place(x=40, y=30)

        self.button_managers = Button(master, text="Менеджери", command=self.menu_managers)
        self.button_managers.place(x=33, y=70)

        self.button_contracts = Button(master, text="Контракти", command=self.menu_contracts)
        self.button_contracts.place(x=36, y=110)

        self.button_requests = Button(master, text="Запроси", command=self.menu_requests)
        self.button_requests.place(x=40, y=150)

        self.button_exit = Button(master, text="Вихід з програми", command=self.exit_program)
        self.button_exit.place(x=20, y=190)

    def menu_clients(self):
        clients_window = Tk()
        clients_window.title("Інформація про клієнтів")
        clients_window.geometry("490x250")

        add_client_button = Button(clients_window, text="Додати клієнта", command=lambda: Client.add_client(self.db))
        add_client_button.place(x=10, y=10)

        delete_client_button = Button(clients_window, text="Видалити клієнта", command=lambda: Client.delete_client(self.db))
        delete_client_button.place(x=10, y=50)

        clients_listbox = Listbox(clients_window, width=57, height=14)
        clients_listbox.place(x=130, y=10)

        clients = Client.list_clients(self.db)
        for client in clients:
            client_info = f" ID: {client[0]}  —  {client[2]}  —  {client[1]}"
            clients_listbox.insert("end", client_info)

        back_button = Button(clients_window, text="Назад", command=clients_window.destroy)
        back_button.place(x=10, y=90)

    def menu_managers(self):
        managers_window = Tk()
        managers_window.title("Інформація про менеджерів")
        managers_window.geometry("490x250")

        add_manager_button = Button(managers_window, text="Додати менеджера", command=lambda: Manager.add_manager(self.db))
        add_manager_button.place(x=10, y=10)

        delete_manager_button = Button(managers_window, text="Видалити менеджера", command=lambda: Manager.delete_manager(self.db))
        delete_manager_button.place(x=10, y=50)

        managers_listbox = Listbox(managers_window, width=57, height=14)
        managers_listbox.place(x=140, y=10)

        managers = Manager.list_managers(self.db)
        for manager in managers:
            manager_info = f" ID: {manager[0]}  —  {manager[2]}  —  {manager[1]}"
            managers_listbox.insert("end", manager_info)

        back_button = Button(managers_window, text="Назад", command=managers_window.destroy)
        back_button.place(x=10, y=90)

    def menu_contracts(self):
        contracts_window = Tk()
        contracts_window.title("Інформація про контракти")
        contracts_window.geometry("500x290")

        add_contract_button = Button(contracts_window, text="Додати контракт", command=lambda: Contract.add_contract(self.db))
        add_contract_button.place(x=10, y=10)

        delete_contract_button = Button(contracts_window, text="Видалити контракт", command=lambda: Contract.delete_contract(self.db))
        delete_contract_button.place(x=10, y=50)

        details_button = Button(contracts_window, text="Детальніша інформація", command=self.contract_details)
        details_button.place(x=10, y=90)

        self.contracts_listbox = Listbox(contracts_window, width=50, height=16)
        self.contracts_listbox.place(x=170, y=10)

        contracts = Contract.list_contracts(self.db)
        for contract in contracts:
            contract_info = f" ID: {contract[0]}  —  {contract[2]}  —  {contract[1]}"
            self.contracts_listbox.insert("end", contract_info)

        back_button = Button(contracts_window, text="Назад", command=contracts_window.destroy)
        back_button.place(x=10, y=140)

    def contract_details(self):
        selected_index = self.contracts_listbox.curselection()
        if selected_index:
            contract_id = int(selected_index[0]) + 1
            contract_details = Contract.get_contract_details(self.db, contract_id)
            if contract_details:
                DetailsWindow(contract_details)

    def menu_requests(self):
        request_window = Tk()
        request_window.title("Меню запроcів")
        request_window.geometry("220x170")

        Button(request_window, text="Кількість торговельних точок", command=lambda: count_trading_points(self.db)).place(x=20, y=10)
        Button(request_window, text="Список типів торговельних точок", command=lambda: list_trading_point_types(self.db)).place(x=10, y=40)
        Button(request_window, text="Самий довгий контракт", command=lambda: longest_contract(self.db)).place(x=37, y=70)
        Button(request_window, text="Самий дорогий контракт", command=lambda: most_expensive_contract(self.db)).place(x=33, y=100)
        Button(request_window, text="Середній термін оренди", command=lambda: calculate_average_rental_term(self.db)).place(x=35, y=130)

    def exit_program(self):
        self.master.destroy()


def main():
    root = Tk()
    FoodMarketApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
