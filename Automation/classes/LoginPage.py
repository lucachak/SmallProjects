from customtkinter import *
from PIL import Image

class LoginPage(CTkFrame):
    def __init__(self, master, on_login, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_login = on_login
        self._setup_layout()
        self._create_login_form()

    def _setup_layout(self):
        """Setup grid layout for centering"""
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def _create_login_form(self):
        """Create login form elements"""
        center_frame = CTkFrame(self, fg_color="transparent")
        center_frame.grid(row=1, column=1, sticky="nsew")

        self._create_banner(center_frame)
        self._create_input_fields(center_frame)

    def _create_banner(self, parent):
        """Create logo/title banner"""
        banner_frame = CTkFrame(parent, fg_color="transparent")
        banner_frame.pack(pady=20, fill="x")

        try:
            logo_original = Image.open("logo.png")
            logo_img = CTkImage(logo_original, size=(120, 120))
            banner_label = CTkLabel(banner_frame, image=logo_img, text="")
            banner_label.image = logo_img
        except Exception:
            banner_label = CTkLabel(
                banner_frame,
                text="Minha Logo",
                font=("Arial", 28, "bold")
            )
        banner_label.pack(anchor="center")

    def _create_input_fields(self, parent):
        """Create login input fields"""
        form_frame = CTkFrame(parent, fg_color="transparent")
        form_frame.pack(pady=10, fill="x")

        # Username field
        self.username_entry = CTkEntry(form_frame, placeholder_text="Usuário")
        self.username_entry.pack(pady=5, padx=20, fill="x")
        self.username_entry.bind("<Return>", lambda e: self._attempt_login())

        # Password field
        self.password_entry = CTkEntry(form_frame, placeholder_text="Senha", show="*")
        self.password_entry.pack(pady=5, padx=20, fill="x")
        self.password_entry.bind("<Return>", lambda e: self._attempt_login())

        # Remember me checkbox
        self.remember_var = BooleanVar()
        CTkCheckBox(
            form_frame, 
            text="Lembrar-me", 
            variable=self.remember_var
        ).pack(pady=10, anchor="w", padx=20)

        # Login button
        CTkButton(
            form_frame, 
            text="Login", 
            command=self._attempt_login
        ).pack(pady=15, padx=20, fill="x")

        # Feedback label
        self.feedback = CTkLabel(form_frame, text="", text_color="red")
        self.feedback.pack(pady=10)

    def _attempt_login(self):
        """Attempt user login"""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "lucas" and password == "lucas":
            self.feedback.configure(text="Login bem-sucedido!", text_color="green")
            self.on_login(username)
        else:
            self.feedback.configure(text="Usuário ou senha incorretos!", text_color="red")
