import os
from tkinter import ttk
from .EmailHandler import EmailHandler
from customtkinter import *
from .ExcelHandler import ExcelHandler

class Page4(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color="transparent")
        email_handler = EmailHandler()
        excel_handler = ExcelHandler(email_handler=email_handler)

        CTkLabel(self,
                 text="Excel Automation",
                 font=("Arial", 16)).grid(
                         row=0, column=0, sticky="w", padx=10, pady=10 
                         )

        
        CTkFrame(self, corner_radius=10).grid(pady=20, padx=20)
        CTkButton(self, text="Select Excel File", command=excel_handler.select_file).grid(pady=20)
        CTkLabel(self, text="No file processed yet.").grid(pady=10)

