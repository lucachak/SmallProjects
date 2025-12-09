#!/home/lucas/Documents/Python/Automation/.venv/bin/python3
import sqlite3
from customtkinter import *


class DBManager:
    def __init__(self, db_name="database.db", terminal=None):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.terminal = terminal

    def log(self, msg):
        if self.terminal:
            self.terminal.append_text(msg)
        else:
            print(msg)

    def create_table(self, name):
        self.cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {name}(id INTEGER PRIMARY KEY, value TEXT)
        """)
        self.conn.commit()
        self.log(f"[+] Table '{name}' ready.\n")

    def insert_item(self, table, value):
        self.cursor.execute(f"INSERT INTO {table}(value) VALUES(?)", (value,))
        self.conn.commit()
        self.log(f"[+] Inserted '{value}' into '{table}'.\n")

    def get_all_items(self, table):
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        self.log(f"[+] All items from '{table}':{rows}\n")
        return rows

    def get_all_tables(self):
        self.cursor.execute("""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table'
                            """)
        tables = [row[0] for row in self.cursor.fetchall()]
        self.log(f"[+] Tables: {tables}\n")
        return tables

    def get_item_by_id(self, table, item_id):
        self.cursor.execute(f"SELECT * FROM {table} WHERE id=?", (item_id,))
        row = self.cursor.fetchone()
        self.log(f"[+] Item with id={item_id} from '{table}': {row}\n")
        return row

    def close_conn(self):
        self.conn.close()
        self.log("[+] Connection closed.\n")

