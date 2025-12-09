# dashboard.py
from customtkinter import *
import datetime


class Dashboard(CTkFrame):
    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, fg_color="#e8f4f8", **kwargs)
        self.navigate_callback = navigate_callback

        # Sidebar
        self._setup_sidebar()

        # Main content
        self._setup_main_content()

    def _setup_sidebar(self):
        """Create left sidebar"""
        sidebar = CTkFrame(self, fg_color="#1e3a8a", width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Profile section
        profile_frame = CTkFrame(sidebar, fg_color="transparent")
        profile_frame.pack(pady=30, padx=20)
        
        profile_pic = CTkFrame(profile_frame, fg_color="#3b82f6", width=60, height=60, corner_radius=30)
        profile_pic.pack()
        profile_pic.pack_propagate(False)
        CTkLabel(profile_pic, text="👤", font=("Arial", 24)).pack(expand=True)

        # Navigation buttons
        nav_buttons = [
            ("☁️  My cloud", "Dashboard", True),
            ("👥  Shared files", "Dashboard", False),
            ("⭐  Favorites", "Dashboard", False),
            ("📁  File Manager", "FileManager", False),
            ("⚙️  API Manager", "ApiManager", False)
        ]

        for text, page, is_active in nav_buttons:
            btn = CTkButton(
                sidebar,
                text=text,
                command=lambda p=page: self.navigate_callback(p),
                fg_color="#2563eb" if is_active else "transparent",
                hover_color="#2563eb",
                anchor="w",
                height=40,
                font=("Arial", 14)
            )
            btn.pack(fill="x", padx=15, pady=5)

        # Spacer
        CTkFrame(sidebar, fg_color="transparent", height=20).pack(expand=True)
        
        # Bottom buttons
        CTkButton(
            sidebar,
            text="⚙️  Settings",
            command=lambda: None,
            fg_color="transparent",
            hover_color="#2563eb",
            anchor="w",
            height=40,
            font=("Arial", 14)
        ).pack(fill="x", padx=15, pady=5, side="bottom")
        
        CTkButton(
            sidebar,
            text="🚪  Log out",
            command=lambda: self.navigate_callback("LoginPage"),
            fg_color="transparent",
            hover_color="#2563eb",
            anchor="w",
            height=40,
            font=("Arial", 14)
        ).pack(fill="x", padx=15, pady=5, side="bottom")

    def _setup_main_content(self):
        """Create main dashboard content"""
        main = CTkScrollableFrame(self, fg_color="transparent")
        main.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        
        # Enable mouse wheel scrolling for all platforms
        self._enable_mousewheel_scrolling(main)

        # Welcome header with date/time
        self._setup_welcome_header(main)

        # Stats cards row
        self._setup_stats_cards(main)

        # Quick actions
        self._setup_quick_actions(main)

        # Two column layout for recent activity and storage
        columns = CTkFrame(main, fg_color="transparent")
        columns.pack(fill="both", expand=True, pady=(20, 0))

        left_col = CTkFrame(columns, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))

        right_col = CTkFrame(columns, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True)

        # Recent activity
        self._setup_recent_activity(left_col)

        # Storage and shared folders
        self._setup_storage_info(right_col)

    def _enable_mousewheel_scrolling(self, widget):
        """Enable smooth mouse wheel scrolling for all platforms"""
        def _on_mousewheel(event):
            # Windows and macOS
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _on_mousewheel_linux(event):
            # Linux uses different events
            if event.num == 4:
                widget._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                widget._parent_canvas.yview_scroll(1, "units")
        
        def _bind_to_mousewheel(event):
            # Windows and macOS
            widget._parent_canvas.bind_all("<MouseWheel>", _on_mousewheel)
            # Linux
            widget._parent_canvas.bind_all("<Button-4>", _on_mousewheel_linux)
            widget._parent_canvas.bind_all("<Button-5>", _on_mousewheel_linux)
        
        def _unbind_from_mousewheel(event):
            widget._parent_canvas.unbind_all("<MouseWheel>")
            widget._parent_canvas.unbind_all("<Button-4>")
            widget._parent_canvas.unbind_all("<Button-5>")
        
        widget.bind("<Enter>", _bind_to_mousewheel)
        widget.bind("<Leave>", _unbind_from_mousewheel)

    def _setup_welcome_header(self, parent):
        """Welcome header with greeting"""
        header = CTkFrame(parent, fg_color="white", corner_radius=15, height=130)
        header.pack(fill="x", pady=(0, 25))
        header.pack_propagate(False)

        header_content = CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=25)

        # Left side - greeting
        left_frame = CTkFrame(header_content, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)

        # Get current hour for greeting
        hour = datetime.datetime.now().hour
        if hour < 12:
            greeting = "Good morning"
        elif hour < 18:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        CTkLabel(
            left_frame,
            text=f"{greeting}, User!",
            font=("Arial", 28, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x")

        date_str = datetime.datetime.now().strftime("%A, %B %d, %Y")
        CTkLabel(
            left_frame,
            text=date_str,
            font=("Arial", 13),
            text_color="#64748b",
            anchor="w"
        ).pack(fill="x", pady=(5, 0))

        # Right side - quick info
        info_frame = CTkFrame(header_content, fg_color="#f8fafc", corner_radius=12)
        info_frame.pack(side="right", padx=(20, 0))

        info_content = CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(padx=20, pady=15)

        CTkLabel(
            info_content,
            text="Total Storage",
            font=("Arial", 11),
            text_color="#64748b"
        ).pack()

        CTkLabel(
            info_content,
            text="75 GB / 100 GB",
            font=("Arial", 16, "bold"),
            text_color="#1e293b"
        ).pack(pady=(2, 0))

    def _setup_stats_cards(self, parent):
        """Statistics cards"""
        stats_frame = CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 25))

        stats = [
            ("Total Files", "1,062", "📄", "#3b82f6", "+12 today"),
            ("Total Size", "75 GB", "💾", "#8b5cf6", "25% left"),
            ("Shared Files", "234", "👥", "#ec4899", "5 new"),
            ("API Status", "Active", "⚙️", "#10b981", "Running"),
        ]

        for i, (title, value, icon, color, subtitle) in enumerate(stats):
            card = CTkFrame(stats_frame, fg_color="white", corner_radius=12)
            card.grid(row=0, column=i, padx=8, sticky="nsew")

            card_content = CTkFrame(card, fg_color="transparent")
            card_content.pack(fill="both", padx=20, pady=20)

            # Icon
            icon_bg = CTkFrame(card_content, fg_color=color, width=45, height=45, corner_radius=10)
            icon_bg.pack(anchor="w")
            icon_bg.pack_propagate(False)
            CTkLabel(icon_bg, text=icon, font=("Arial", 20)).pack(expand=True)

            # Value
            CTkLabel(
                card_content,
                text=value,
                font=("Arial", 24, "bold"),
                text_color="#1e293b",
                anchor="w"
            ).pack(fill="x", pady=(12, 2))

            # Title
            CTkLabel(
                card_content,
                text=title,
                font=("Arial", 12),
                text_color="#64748b",
                anchor="w"
            ).pack(fill="x")

            # Subtitle
            CTkLabel(
                card_content,
                text=subtitle,
                font=("Arial", 10, "bold"),
                text_color=color,
                anchor="w"
            ).pack(fill="x", pady=(4, 0))

        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

    def _setup_quick_actions(self, parent):
        """Quick action cards"""
        CTkLabel(
            parent,
            text="Quick Actions",
            font=("Arial", 20, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))

        actions_grid = CTkFrame(parent, fg_color="transparent")
        actions_grid.pack(fill="x", pady=(0, 10))

        actions = [
            {
                "title": "File Manager",
                "desc": "Upload and organize files",
                "icon": "📁",
                "color": "#3b82f6",
                "page": "FileManager"
            },
            {
                "title": "API Manager",
                "desc": "Control API services",
                "icon": "⚙️",
                "color": "#8b5cf6",
                "page": "ApiManager"
            },
            {
                "title": "Shared Folders",
                "desc": "Collaborate with others",
                "icon": "👥",
                "color": "#ec4899",
                "page": "Dashboard"
            }
        ]

        for i, action in enumerate(actions):
            card = CTkFrame(actions_grid, fg_color="white", corner_radius=12, cursor="hand2")
            card.grid(row=0, column=i, padx=8, sticky="nsew")

            card.bind("<Button-1>", lambda e, p=action["page"]: self.navigate_callback(p))

            card_content = CTkFrame(card, fg_color="transparent")
            card_content.pack(fill="both", padx=25, pady=25)

            # Icon
            icon_frame = CTkFrame(card_content, fg_color=action["color"], width=55, height=55, corner_radius=12)
            icon_frame.pack(anchor="w")
            icon_frame.pack_propagate(False)
            
            icon_label = CTkLabel(icon_frame, text=action["icon"], font=("Arial", 26))
            icon_label.pack(expand=True)
            icon_label.bind("<Button-1>", lambda e, p=action["page"]: self.navigate_callback(p))

            # Title
            title_label = CTkLabel(
                card_content,
                text=action["title"],
                font=("Arial", 16, "bold"),
                text_color="#1e293b",
                anchor="w"
            )
            title_label.pack(fill="x", pady=(15, 5))
            title_label.bind("<Button-1>", lambda e, p=action["page"]: self.navigate_callback(p))

            # Description
            desc_label = CTkLabel(
                card_content,
                text=action["desc"],
                font=("Arial", 12),
                text_color="#64748b",
                anchor="w"
            )
            desc_label.pack(fill="x")
            desc_label.bind("<Button-1>", lambda e, p=action["page"]: self.navigate_callback(p))

            # Arrow
            arrow_label = CTkLabel(card_content, text="→", font=("Arial", 20), text_color="#94a3b8")
            arrow_label.pack(anchor="e", pady=(10, 0))
            arrow_label.bind("<Button-1>", lambda e, p=action["page"]: self.navigate_callback(p))

        for i in range(3):
            actions_grid.grid_columnconfigure(i, weight=1)

    def _setup_recent_activity(self, parent):
        """Recent activity section"""
        CTkLabel(
            parent,
            text="Recent Activity",
            font=("Arial", 18, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))

        activity_card = CTkFrame(parent, fg_color="white", corner_radius=15)
        activity_card.pack(fill="both", expand=True)

        activities = [
            ("📄 Document uploaded", "Work_Report.pdf", "2 min ago", "#3b82f6"),
            ("👥 File shared", "Project_Plan.docx", "15 min ago", "#ec4899"),
            ("⚙️ API started", "Development server", "1 hour ago", "#10b981"),
            ("📷 Image added", "Screenshot_2024.png", "2 hours ago", "#8b5cf6"),
            ("📁 Folder created", "New Project", "3 hours ago", "#06b6d4"),
        ]

        for title, subtitle, time, color in activities:
            activity_item = CTkFrame(activity_card, fg_color="transparent", height=70)
            activity_item.pack(fill="x", padx=20, pady=8)
            activity_item.pack_propagate(False)

            # Icon
            icon_bg = CTkFrame(activity_item, fg_color=color, width=45, height=45, corner_radius=10)
            icon_bg.pack(side="left", padx=(0, 12), pady=(0,18))
            icon_bg.pack_propagate(False)
            CTkLabel(icon_bg, text=title.split()[0], font=("Arial", 18)).pack(expand=True)

            # Info
            info_frame = CTkFrame(activity_item, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)

            CTkLabel(
                info_frame,
                text=title,
                font=("Arial", 13, "bold"),
                text_color="#1e293b",
                anchor="w"
            ).pack(fill="x")

            CTkLabel(
                info_frame,
                text=subtitle,
                font=("Arial", 11),
                text_color="#64748b",
                anchor="w"
            ).pack(fill="x")

            # Time
            CTkLabel(
                activity_item,
                text=time,
                font=("Arial", 11),
                text_color="#94a3b8"
            ).pack(side="right", padx=(10, 0))

    def _setup_storage_info(self, parent):
        """Storage and shared folders info"""
        # Storage section
        CTkLabel(
            parent,
            text="Storage Usage",
            font=("Arial", 18, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))

        storage_card = CTkFrame(parent, fg_color="white", corner_radius=15)
        storage_card.pack(fill="x", pady=(0, 20))

        storage_content = CTkFrame(storage_card, fg_color="transparent")
        storage_content.pack(fill="both", padx=25, pady=25)

        # Header with percentage
        storage_header = CTkFrame(storage_content, fg_color="transparent")
        storage_header.pack(fill="x")

        CTkLabel(
            storage_header,
            text="75 GB of 100 GB",
            font=("Arial", 16, "bold"),
            text_color="#1e293b"
        ).pack(side="left")

        CTkLabel(
            storage_header,
            text="25% free",
            font=("Arial", 13, "bold"),
            text_color="#3b82f6"
        ).pack(side="right")

        # Progress bar
        progress_bar = CTkProgressBar(
            storage_content,
            height=12,
            corner_radius=6,
            progress_color="#3b82f6"
        )
        progress_bar.pack(fill="x", pady=15)
        progress_bar.set(0.75)

        # Storage breakdown
        breakdown = [
            ("Documents", "35 GB", "#3b82f6"),
            ("Images", "25 GB", "#8b5cf6"),
            ("Videos", "10 GB", "#ec4899"),
            ("Other", "5 GB", "#64748b"),
        ]

        for label, size, color in breakdown:
            item_frame = CTkFrame(storage_content, fg_color="transparent")
            item_frame.pack(fill="x", pady=4)

            color_dot = CTkFrame(item_frame, fg_color=color, width=12, height=12, corner_radius=6)
            color_dot.pack(side="left", padx=(0, 8))
            color_dot.pack_propagate(False)

            CTkLabel(
                item_frame,
                text=label,
                font=("Arial", 12),
                text_color="#64748b"
            ).pack(side="left")

            CTkLabel(
                item_frame,
                text=size,
                font=("Arial", 12, "bold"),
                text_color="#1e293b"
            ).pack(side="right")

        # Upgrade button
        CTkButton(
            storage_content,
            text="Upgrade Storage",
            height=38,
            corner_radius=10,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Arial", 13, "bold")
        ).pack(fill="x", pady=(15, 0))

        # Shared folders
        CTkLabel(
            parent,
            text="Your Shared Folders",
            font=("Arial", 18, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(10, 15))

        shared_card = CTkFrame(parent, fg_color="white", corner_radius=15)
        shared_card.pack(fill="both", expand=True)

        folders = [
            ("Keynote files", ["👤", "👤"], "#8b5cf6"),
            ("Vacation photos", ["👤"], "#ec4899"),
            ("Project report", ["👤", "👤"], "#3b82f6"),
        ]

        for name, users, color in folders:
            folder_item = CTkFrame(shared_card, fg_color="#f8fafc", corner_radius=10, height=65)
            folder_item.pack(fill="x", padx=20, pady=8)
            folder_item.pack_propagate(False)

            folder_content = CTkFrame(folder_item, fg_color="transparent")
            folder_content.pack(fill="both", padx=15, pady=12)

            # Icon
            icon_bg = CTkFrame(folder_content, fg_color=color, width=40, height=40, corner_radius=8)
            icon_bg.pack(side="left", padx=(0, 12))
            icon_bg.pack_propagate(False)
            CTkLabel(icon_bg, text="📁", font=("Arial", 18)).pack(expand=True)

            # Name
            CTkLabel(
                folder_content,
                text=name,
                font=("Arial", 13, "bold"),
                text_color="#1e293b",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

            # User avatars
            users_frame = CTkFrame(folder_content, fg_color="transparent")
            users_frame.pack(side="right")

            for i, user in enumerate(users):
                user_avatar = CTkFrame(users_frame, fg_color="#cbd5e1", width=28, height=28, corner_radius=14)
                user_avatar.pack(side="left", padx=2)
                user_avatar.pack_propagate(False)
                CTkLabel(user_avatar, text=user, font=("Arial", 12)).pack(expand=True)

        # Add more button
        CTkButton(
            shared_card,
            text="+ Add more",
            fg_color="transparent",
            text_color="#64748b",
            hover_color="#f1f5f9",
            height=30,
            font=("Arial", 12)
        ).pack(pady=(5, 15))

