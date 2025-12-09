# login_page.py
from customtkinter import CTkFrame, CTkEntry, CTkButton, CTkLabel


class LoginPage(CTkFrame):
    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, fg_color="#e8f4f8", **kwargs)
        self.navigate_callback = navigate_callback

        # Center container (using pack instead of place for better compatibility)
        center_frame = CTkFrame(self, fg_color="#e8f4f8")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Login card
        login_card = CTkFrame(center_frame, fg_color="white", corner_radius=20, width=500, height=600)
        login_card.pack()
        login_card.pack_propagate(False)

        # Logo/Icon
        logo_frame = CTkFrame(login_card, fg_color="#3b82f6", width=80, height=80, corner_radius=40)
        logo_frame.pack(pady=(40, 20))
        logo_frame.pack_propagate(False)
        CTkLabel(logo_frame, text="☁️", font=("Arial", 40)).pack(expand=True)

        # Title
        CTkLabel(
            login_card,
            text="Welcome Back",
            font=("Arial", 26, "bold"),
            text_color="#1e293b"
        ).pack(pady=(0, 5))

        CTkLabel(
            login_card,
            text="Sign in to continue",
            font=("Arial", 13),
            text_color="#64748b"
        ).pack(pady=(0, 30))

        # Username field
        username_container = CTkFrame(login_card, fg_color="transparent")
        username_container.pack(padx=40, pady=10, fill="x")
        
        CTkLabel(
            username_container,
            text="Username",
            font=("Arial", 12, "bold"),
            text_color="#475569",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.username_entry = CTkEntry(
            username_container,
            placeholder_text="Enter your username",
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="#e2e8f0",
            fg_color="white",
            text_color="black",
            font=("Arial", 13)
        )
        self.username_entry.pack(fill="x")

        # Password field
        password_container = CTkFrame(login_card, fg_color="transparent")
        password_container.pack(padx=40, pady=10, fill="x")
        
        CTkLabel(
            password_container,
            text="Password",
            font=("Arial", 12, "bold"),
            text_color="#475569",
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        self.password_entry = CTkEntry(
            password_container,
            placeholder_text="Enter your password",
            show="*",
            height=45,
            corner_radius=10,
            border_width=2,
            border_color="#e2e8f0",
            text_color="black",
            fg_color="white",
            font=("Arial", 13)
        )
        self.password_entry.pack(fill="x")

        # Forgot password
        CTkButton(
            login_card,
            text="Forgot password?",
            fg_color="transparent",
            text_color="#3b82f6",
            hover_color="#f1f5f9",
            font=("Arial", 11),
            height=20,
            command=lambda: None
        ).pack(pady=(5, 20))

        # Login button
        self.login_button = CTkButton(
            login_card,
            text="Sign In",
            command=self.on_login,
            height=45,
            corner_radius=10,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Arial", 14, "bold")
        )
        self.login_button.pack(padx=40, fill="x", pady=(0, 20))

        # Sign up link
        signup_frame = CTkFrame(login_card, fg_color="transparent")
        signup_frame.pack()
        
        CTkLabel(
            signup_frame,
            text="Don't have an account?",
            font=("Arial", 11),
            text_color="#64748b"
        ).pack(side="left", padx=(0, 5))
        
        CTkButton(
            signup_frame,
            text="Sign up",
            fg_color="transparent",
            text_color="#3b82f6",
            hover_color="#3b82f6",
            font=("Arial", 11, "bold"),
            width=60,
            command=lambda: None
        ).pack(side="left")

        # Bind Enter key
        self.password_entry.bind("<Return>", lambda event: self.on_login())
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())

    def on_login(self):
        """Handle login and navigate to dashboard"""
        # Add authentication logic here
        self.navigate_callback("Dashboard")
