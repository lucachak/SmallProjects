from customtkinter import *
from PIL import Image, ImageDraw
import os

class FileManagerApp(CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, fg_color="transparent")
        
        # Configuration
        self.primary_color = "#6366f1"
        self.secondary_color = "#8b5cf6"
        self.bg_color = "#f8fafc"
        self.card_color = "#ffffff"
        
        self.master_app = master
        self.main_app = None

        self._setup_layout()
        self._create_sidebar()
        self._create_main_content()

    def _setup_layout(self):
        """Setup main grid layout"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def set_main_app(self, main_app):
        """Set reference to main app for navigation"""
        self.main_app = main_app

    def _create_sidebar(self):
        """Create sidebar navigation"""
        sidebar = CTkFrame(self, width=240, corner_radius=0,
                         fg_color=("#f1f5f9", "#1e293b"))
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(8, weight=1)

        self._create_sidebar_header(sidebar)
        self._create_sidebar_navigation(sidebar)
        self._create_sidebar_footer(sidebar)

    def _create_sidebar_header(self, parent):
        """Create sidebar header with logo"""
        logo_frame = CTkFrame(parent, fg_color="transparent", height=80)
        logo_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        logo_frame.grid_propagate(False)

        CTkLabel(logo_frame, text="☁️ CloudSpace", 
                font=CTkFont(size=22, weight="bold", family="Segoe UI")
        ).grid(row=0, column=0, sticky="w")

        CTkLabel(logo_frame, text="Your files, everywhere",
                text_color=("gray60", "gray60"),
                font=CTkFont(size=12)
        ).grid(row=1, column=0, sticky="w", pady=(2, 0))

    def _create_sidebar_navigation(self, parent):
        """Create sidebar navigation items"""
        nav_items = [
            ("📁", "All Files"),
            ("🔄", "Sync Now"), 
            ("⭐", "Favorites"),
            ("👥", "Shared"),
            ("📊", "Analytics"),
            ("⚙️", "Settings"),
        ]
        
        for i, (icon, text) in enumerate(nav_items, 1):
            CTkButton(parent, text=f"  {icon}  {text}", 
                     fg_color="transparent", 
                     hover_color=("gray85", "gray30"),
                     anchor="w", 
                     font=CTkFont(size=14, family="Segoe UI"),
                     height=45
            ).grid(row=i, column=0, padx=15, pady=2, sticky="ew")

        # Back to main button
        CTkButton(parent, 
                 text="← Back to Main",
                 command=self._go_to_main,
                 fg_color="#3b82f6",
                 hover_color="#2563eb",
                 text_color="white",
                 font=CTkFont(size=13, weight="bold"),
                 height=35
        ).grid(row=8, column=0, sticky="ew", padx=15, pady=10)

    def _create_sidebar_footer(self, parent):
        """Create sidebar footer with user info"""
        user_frame = CTkFrame(parent, fg_color=("gray90", "gray20"))
        user_frame.grid(row=9, column=0, sticky="ew", padx=15, pady=20)
        
        CTkLabel(user_frame, text="👤", font=CTkFont(size=16)
        ).grid(row=0, column=0, padx=10, pady=10)
        
        CTkLabel(user_frame, text="Alex Morgan\nPremium Plan", 
                font=CTkFont(size=12), justify="left"
        ).grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")

    def _create_main_content(self):
        """Create main content area"""
        main_frame = CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=25)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Scrollable content
        self.scrollable_frame = CTkScrollableFrame(main_frame, fg_color="transparent")
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        self._create_header(self.scrollable_frame)
        self._create_quick_stats(self.scrollable_frame)
        self._create_categories(self.scrollable_frame)
        self._create_recent_files(self.scrollable_frame)
        self._create_storage_info(self.scrollable_frame)

    def _create_header(self, parent):
        """Create main header with search"""
        header_frame = CTkFrame(parent, fg_color="transparent", height=80)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_propagate(False)

        # Welcome message
        CTkLabel(header_frame, 
                text="👋 Welcome back, Alex!",
                font=CTkFont(size=24, weight="bold", family="Segoe UI")
        ).grid(row=0, column=0, sticky="w")

        # Search bar
        search_frame = CTkFrame(header_frame, height=45, corner_radius=12)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        
        CTkEntry(search_frame, 
                placeholder_text="🔍 Search files...",
                border_width=0, 
                height=35,
                font=CTkFont(size=14)
        ).pack(fill="both", expand=True, padx=2, pady=2)

        # Action buttons
        action_frame = CTkFrame(header_frame, fg_color="transparent")
        action_frame.grid(row=0, column=1, rowspan=2, padx=(20, 0), sticky="ns")
        
        CTkButton(action_frame, text="📁 Upload Files", 
                 fg_color=self.primary_color, 
                 hover_color=self.secondary_color,
                 font=CTkFont(weight="bold"), width=120
        ).pack(side="left", padx=(0, 10))
        
        CTkButton(action_frame, text="➕ New Folder",
                 fg_color="transparent", border_width=2,
                 text_color=("gray10", "gray90"), width=120
        ).pack(side="left")

    def _create_quick_stats(self, parent):
        """Create quick stats cards"""
        stats_frame = CTkFrame(parent, fg_color="transparent")
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 25))
        
        stats_data = [
            ("📁", "1,471", "Total Files", "#10b981"),
            ("👥", "24", "Shared", "#f59e0b"),
            ("🔄", "87", "Synced", "#3b82f6"),
            ("⭐", "156", "Favorites", "#ef4444")
        ]
        
        for i, (icon, count, label, color) in enumerate(stats_data):
            self._create_stat_card(stats_frame, icon, count, label, i)

    def _create_stat_card(self, parent, icon, count, label, index):
        """Create individual stat card"""
        card = CTkFrame(parent, height=100, corner_radius=16,
                      fg_color=("white", "gray10"))
        card.grid(row=0, column=index, padx=(0, 15), sticky="nsew")
        card.grid_propagate(False)
        card.grid_columnconfigure(0, weight=1)

        CTkLabel(card, text=icon, font=CTkFont(size=20)
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20, 5))

        CTkLabel(card, text=count, font=CTkFont(size=24, weight="bold")
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 5))

        CTkLabel(card, text=label, text_color=("gray40", "gray60"),
                font=CTkFont(size=12)
        ).grid(row=2, column=0, sticky="w", padx=20, pady=(0, 20))

        parent.grid_columnconfigure(index, weight=1)

    def _create_categories(self, parent):
        """Create categories grid"""
        CTkLabel(parent, text="Categories",
                font=CTkFont(size=18, weight="bold", family="Segoe UI")
        ).grid(row=2, column=0, sticky="w", pady=(0, 15))

        categories_frame = CTkFrame(parent, fg_color="transparent")
        categories_frame.grid(row=3, column=0, sticky="ew", pady=(0, 25))

        categories = [
            ("🖼️", "Pictures", "450 files"),
            ("📄", "Documents", "90 files"),
            ("🎥", "Videos", "30 files"),
            ("🎵", "Audio", "60 files"),
            ("💼", "Work", "820 files"),
            ("🏠", "Personal", "16 files"),
            ("🎓", "School", "65 files"),
            ("📦", "Archive", "21 files")
        ]
        
        for i in range(2):  # 2 rows
            for j in range(4):  # 4 columns
                idx = i * 4 + j
                if idx < len(categories):
                    self._create_category_card(categories_frame, categories[idx], i, j)

    def _create_category_card(self, parent, category_data, row, col):
        """Create individual category card"""
        icon, name, count = category_data
        
        card = CTkFrame(parent, height=80, corner_radius=14,
                      fg_color=("white", "gray10"))
        card.grid(row=row, column=col, padx=(0, 15), pady=(0, 15), sticky="nsew")
        card.grid_columnconfigure(1, weight=1)
        card.grid_propagate(False)

        CTkLabel(card, text=icon, font=CTkFont(size=18)
        ).grid(row=0, column=0, rowspan=2, padx=(15, 10), pady=15, sticky="ns")

        CTkLabel(card, text=name, font=CTkFont(size=14, weight="bold")
        ).grid(row=0, column=1, sticky="w", pady=(15, 0))

        CTkLabel(card, text=count, text_color=("gray40", "gray60"),
                font=CTkFont(size=12)
        ).grid(row=1, column=1, sticky="w", pady=(0, 15))

        parent.grid_columnconfigure(col, weight=1)

    def _create_recent_files(self, parent):
        """Create recent files table"""
        CTkLabel(parent, text="Recent Files",
                font=CTkFont(size=18, weight="bold", family="Segoe UI")
        ).grid(row=4, column=0, sticky="w", pady=(0, 15))

        # Implementation for recent files table would go here
        # (keeping it concise for this example)

    def _create_storage_info(self, parent):
        """Create storage information section"""
        storage_frame = CTkFrame(parent, height=200, corner_radius=16,
                               fg_color=("white", "gray10"))
        storage_frame.grid(row=6, column=0, sticky="ew", pady=25)
        storage_frame.grid_columnconfigure(0, weight=1)
        storage_frame.grid_propagate(False)

        CTkLabel(storage_frame, text="📊 Storage Overview",
                font=CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=25, pady=(25, 15))

        # Storage progress bar and info would go here

    def _go_to_main(self):
        """Navigate back to main page"""
        if self.main_app and hasattr(self.main_app, 'show_page'):
            try:
                from classes.Page1 import Page1
                self.main_app.show_page(Page1)
            except ImportError:
                print("Page1 not found, cannot navigate back")
