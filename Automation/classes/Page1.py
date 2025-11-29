#!/home/lucas/Documents/Python/Automation/.venv/bin/python3 

from .Terminal import Terminal
from customtkinter import *

# -------------------------------
#   CHECKBOX WITHOUT BUTTON
# -------------------------------
class CheckBox(CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master, fg_color="transparent")
        cb_font = ("Arial", 14)
        pad_y = (8, 6)

        self.checkbox_1 = CTkCheckBox(self, text="Clean Computer (Pacman)", font=cb_font)
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=pad_y, sticky="w")

        self.checkbox_2 = CTkCheckBox(self, text="Virus Check", font=cb_font)
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=pad_y, sticky="w")

        self.checkbox_3 = CTkCheckBox(self, text="Create Base Django Project", font=cb_font)
        self.checkbox_3.grid(row=2, column=0, padx=10, pady=pad_y, sticky="w")

        self.checkbox_4 = CTkCheckBox(self, text="Development", font=cb_font)
        self.checkbox_4.grid(row=3, column=0, padx=10, pady=pad_y, sticky="w")

    def get(self):
        """Return selected actions"""
        actions = []
        

        if self.checkbox_1.get() == 1:
            actions.append("clean_pacman")
        if self.checkbox_2.get() == 1:
            actions.append("virus_scanner")
        
        if self.checkbox_3.get() == 1:
            actions.append("django_project")
        return actions


# -------------------------------
#   CHECKBOX WITH INPUT
# -------------------------------

class CheckBoxWithInput(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Expandable column
        self.grid_columnconfigure(0, weight=1)

        # Checkbox
        self.clean_checkbox = CTkCheckBox(self,
            text="🧹 Clean Files",
            command=self.toggle_input
        )
        self.clean_checkbox.grid(row=0, column=0, padx=10, pady=(0,10), sticky="w")

        # Dynamic widgets (start hidden)
        self.input_field = None

    def toggle_input(self):
        """Show or hide input when checkbox is toggled"""
        if self.clean_checkbox.get() == 1:
            if not self.input_field:
                self.input_field = CTkEntry(
                    self,
                    placeholder_text="Digite a pasta..."
                )
                self.input_field.grid(
                    row=1, column=0,
                    padx=10, pady=(0, 10),
                    sticky="ew"
                )
        else:
            if self.input_field:
                self.input_field.destroy()
                self.input_field = None

    def get(self):
        """Return folder if checkbox is checked"""
        if self.clean_checkbox.get() == 1 and self.input_field and self.input_field.get():
            return self.input_field.get()
        return None




class Page1(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        # Terminal panel at the bottom
        self.terminal = Terminal(self)
        self.terminal.grid(row=4, column=0, sticky="nsew")

        self.grid_rowconfigure(3, weight=1)
        
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Content
        self.grid_rowconfigure(2, weight=0)  # Run button
        self.grid_columnconfigure(0, weight=1)

        # Title
        CTkLabel(
            self,
            text="🐧 Linux Control Panel",
            font=("Arial", 18, "bold"),
            text_color="#89b4fa"
        ).grid(row=0, column=0, pady=10)

        # Content frame
        content = CTkFrame(self, fg_color="transparent", corner_radius=15)
        content.grid(row=1, column=0, sticky="nsew")

        # Widgets
        self.checkbox_frame = CheckBox(content)
        self.checkbox_frame.pack(fill="x", padx=20, pady=5)

        self.checkbox_input = CheckBoxWithInput(content)
        self.checkbox_input.pack(fill="x", padx=20, pady=5)

        # Main Run button
        run_btn = CTkButton(
            self, text="▶ Run",
            fg_color="#a6e3a1", hover_color="#8bd97d",
            text_color="black", corner_radius=15,
            command=self.run_actions
        )
        run_btn.grid(row=3, column=0, pady=0)

    def run_actions(self):
        """Collects results from all checkboxes"""
        actions = self.checkbox_frame.get()
        folder = self.checkbox_input.get()

        if "clean_pacman" in actions:
            self.terminal.run_command("pacman", "python3 ./commands/clean_arch.py")
        
        if "virus_scanner" in actions:
            self.terminal.run_command("scanner", "./commands/virus_scanner.py --paths ~ --days 7")

        if "django_project" in actions:
            self.terminal.run_command("django_project", "python3 ./commands/create_django_project.py")

        if "" in actions:
            print("⚠ Empty function selected (not implemented)")

        # Handle folder cleanup
        if folder:
            self.terminal.run_command(f"./commands/clean_file.py {folder}")
            print(f"🗑 Cleaning files in: {folder}")

