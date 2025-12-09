#!/usr/bin/env python3
import os
from customtkinter import *
from .Terminal import Terminal
from .DBManager import DBManager
from tkinter import ttk

class Page2(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Layout
        self.grid_rowconfigure(3, weight=1)   # terminal grows at bottom
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Title
        CTkLabel(self, text="📊 Database Area", font=("Arial", 16)).grid(
            row=0, column=0, sticky="w", padx=10, pady=10
        )

        # Table selector dropdown
        self.table_selector = CTkOptionMenu(self, values=["No tables"], command=self.switch_table)
        self.table_selector.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Input fields
        self.value_entry = CTkEntry(self, placeholder_text="Value to insert")
        self.value_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.id_entry = CTkEntry(self, placeholder_text="ID")
        self.id_entry.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Buttons
        self.btn_create = CTkButton(self, text="➕ Create Table", command=self.create_table)
        self.btn_create.grid(row=1, column=3, padx=5, pady=5)

        self.btn_insert = CTkButton(self, text="📥 Insert Item", command=self.insert_item)
        self.btn_insert.grid(row=1, column=4, padx=5, pady=5)

        self.more_options = CTkOptionMenu(
            self,
            values=["📂 Get All Tables", "📋 Get All Items", "🔍 Get by ID", "📊 Monitor DB"],
            command=self.handle_more_option
        )
        self.more_options.grid(row=1, column=5, padx=5, pady=5)
        self.more_options.set("⋮ More")  # placeholder

        # --- Small stats frame (shows counts inside UI) ---
        stats_frame = CTkFrame(self, fg_color="#1b1b1b")
        stats_frame.grid(row=2, column=0, columnspan=6, sticky="ew", padx=10, pady=(5,0))
        stats_frame.grid_columnconfigure((0,1,2), weight=1)

        self.lbl_tables = CTkLabel(stats_frame, text="Tables: 0")
        self.lbl_tables.grid(row=0, column=0, padx=8, pady=6, sticky="w")

        self.lbl_rows = CTkLabel(stats_frame, text="Total rows: 0")
        self.lbl_rows.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        self.lbl_size = CTkLabel(stats_frame, text="DB size: 0 KB")
        self.lbl_size.grid(row=0, column=2, padx=8, pady=6, sticky="w")

        # --- Scrollable list of tables with per-table counts ---
        self.table_list_frame = CTkScrollableFrame(self, height=120)
        self.table_list_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=6)
        self.table_list_frame.grid_columnconfigure(0, weight=1)

        # Right side: terminal area
        self.terminal = Terminal(self)
        self.terminal.grid(row=3, column=3, columnspan=3, sticky="nsew", padx=5, pady=5)

        # DB manager
        self.db = DBManager(terminal=self.terminal)

        # initial refresh
        self.refresh_tables()

    # -------------------------
    # UI helpers
    # -------------------------
    def refresh_tables(self):
        tables = self.db.get_all_tables()
        if tables:
            self.table_selector.configure(values=tables)
            self.table_selector.set(tables[0])
        else:
            self.table_selector.configure(values=["No tables"])
            self.table_selector.set("No tables")
        # refresh stats & list
        self.refresh_ui()

    def refresh_ui(self):
        # update stats
        tables = self.db.get_all_tables()
        total_rows = 0
        # clear table_list_frame
        for w in self.table_list_frame.winfo_children():
            w.destroy()
        for t in tables:
            rows = self.db.get_all_items(t)
            count = len(rows)
            total_rows += count
            CTkLabel(self.table_list_frame, text=f"{t} — {count} rows").pack(anchor="w", padx=8, pady=2)
        # size
        db_file = "database.db"
        size_kb = os.path.getsize(db_file) / 1024 if os.path.exists(db_file) else 0.0
        self.lbl_tables.configure(text=f"Tables: {len(tables)}")
        self.lbl_rows.configure(text=f"Total rows: {total_rows}")
        self.lbl_size.configure(text=f"DB size: {size_kb:.2f} KB")

    def get_active_table(self):
        selected = self.table_selector.get()
        return selected if selected != "No tables" else None

    # -------------------------
    # Actions
    # -------------------------
    def switch_table(self, name):
        self.terminal.append_text(f"[+] Active table switched to '{name}'\n")

    def create_table(self):
        name = self.value_entry.get().strip()
        if not name:
            self.terminal.append_text("[!] Enter a table name in 'Value' field.\n")
            return
        self.db.create_table(name)
        self.refresh_tables()

    def insert_item(self):
        table = self.get_active_table()
        value = self.value_entry.get().strip()
        if not table or not value:
            self.terminal.append_text("[!] Select table and enter value.\n")
            return
        self.db.insert_item(table, value)
        self.refresh_ui()

    def get_tables(self):
        self.refresh_tables()

    def get_items(self):
        table = self.get_active_table()
        if not table:
            self.terminal.append_text("[!] No table selected.\n")
            return
        self.db.get_all_items(table)
        self.refresh_ui()

    def get_item_by_id(self):
        table = self.get_active_table()
        try:
            item_id = int(self.id_entry.get())
        except ValueError:
            self.terminal.append_text("[!] Enter a valid ID (number).\n")
            return
        if not table:
            self.terminal.append_text("[!] No table selected.\n")
            return
        self.db.get_item_by_id(table, item_id)

    def monitor_db(self):
        # uses refresh_ui which displays stuff in the UI & terminal
        self.refresh_ui()
        self.terminal.append_text("[+] DB monitor refreshed.\n")

    def handle_more_option(self, choice):
        if choice == "📂 Get All Tables":
            self.get_tables()
        elif choice == "📋 Get All Items":
            self.get_items()
        elif choice == "🔍 Get by ID":
            self.get_item_by_id()
        elif choice == "📊 Monitor DB":
            self.monitor_db()
        self.more_options.set("⋮ More")

