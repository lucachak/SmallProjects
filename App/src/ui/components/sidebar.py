# sidebar.py
from customtkinter import CTkFrame, CTkButton


class Sidebar(CTkFrame):
    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, fg_color="#1e3a8a", width=200, **kwargs)
        self.navigate_callback = navigate_callback

        CTkButton(self, text="Dashboard", command=lambda: self.navigate_callback("Dashboard")).pack(pady=10)
        CTkButton(self, text="File Manager", command=lambda: self.navigate_callback("FileManager")).pack(pady=10)
        CTkButton(self, text="API Manager", command=lambda: self.navigate_callback("ApiManager")).pack(pady=10)
        CTkButton(self, text="Logout", command=lambda: self.navigate_callback("LoginPage")).pack(pady=10)
