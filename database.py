import sqlite3


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def open(self):
        self.connection = sqlite3.connect(self.db_file)

    def close(self):
        if self.connection:
            self.connection.close()

    def create_tables(self):
        with sqlite3.connect(self.db_file) as db:
            cursor = db.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS contracts(
                id INTEGER PRIMARY KEY,
                foodMarket_name TEXT,
                product_type TEXT,
                point_number INTEGER,
                start_data INTEGER,
                end_data INTEGER,
                cost INTEGER,
                client_id INTEGER,
                manager_id INTEGER,
                FOREIGN KEY (client_id) REFERENCES persons(name),
                FOREIGN KEY (manager_id) REFERENCES persons(name))''')

            cursor.execute('''CREATE TABLE IF NOT EXISTS persons(
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone_number INTEGER,
                type TEXT)''')


if __name__ == "__main__":
    db_file = 'db/database.db'
    db = Database(db_file)
