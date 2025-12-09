
import sys
from customtkinter import *
from .Terminal import Terminal
from .ApiHandler import ApiHandler

class Page3(CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Terminal (bottom, expanding)
        self.terminal = Terminal(self)  # <-- define terminal first
        self.terminal.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        # ApiHandler (needs terminal)
        self.api_handler = ApiHandler(self.terminal)

        # Configure grid (1 column, multiple rows)
        self.grid_rowconfigure(0, weight=0)   # header row (label)
        self.grid_rowconfigure(1, weight=0)   # button row
        self.grid_rowconfigure(2, weight=1)   # terminal row -> expands
        self.grid_columnconfigure(0, weight=1)

        # Header
        CTkLabel(
            self,
            text="Pagina 3 - Api Control",
            font=("Arial", 16)
        ).grid(row=0, column=0, pady=20, padx=20, sticky="w")

        # Buttons
        self.button_frame = CTkFrame(self, corner_radius=15)
        self.button_frame.grid(row=1, column=0, pady=10, sticky="w")


        CTkButton(
            self.button_frame,   # <-- use button_frame as parent
            text="Start API",
            fg_color="#a6e3a1",
            text_color="black",
            corner_radius=15,
            command=self.api_handler.start_api
        ).pack(side="left", padx=5)

        CTkButton(
            self.button_frame,
            text="Stop API",
            fg_color="#f38ba8",
            text_color="black",
            corner_radius=15,
            command=self.api_handler.stop_api
        ).pack(side="left", padx=5)

    
        self.Api_Mass_test = CTkFrame(self, corner_radius=15)
        self.Api_Mass_test.grid(row=1, column=1, pady=10, sticky="e")

        CTkButton(
                self.Api_Mass_test,
                text="Mass Spam",
                fg_color="#dddddd",
                text_color="black",
                corner_radius=15,
                command=lambda:print("Func")
                ).pack(side="left",padx=5)


    # ---------------- Utils ----------------
    def _check_requirements(self):
        import importlib
        installed = []
        for lib in ["flask", "fastapi"]:
            if importlib.util.find_spec(lib) is not None:
                installed.append(lib)
        return installed

    def start_api(self):
        self.terminal.run_command("Running Api...", f"{sys.executable} ./commands/start_api.py")
        self.api_handler.start_api()

    def stop_api(self):
        self.api_handler.stop_api()

