# topbar.py
from customtkinter import CTkFrame, CTkEntry, CTkLabel


class TopBar(CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#f1f5f9", height=60, **kwargs)
        self.pack_propagate(False)

        # Search bar
        search = CTkEntry(self, placeholder_text="Search...", width=300)
        search.pack(side="left", padx=20, pady=10)

        # User info on the right
        user_frame = CTkFrame(self, fg_color="transparent")
        user_frame.pack(side="right", padx=20, pady=10)

        CTkLabel(user_frame, text="Welcome, User!").pack(side="right", padx=10)
