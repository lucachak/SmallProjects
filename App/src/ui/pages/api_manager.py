# api_manager.py
from customtkinter import *
import datetime
import os
import sys

# Import the Flask server manager
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
try:
    from src.core.flask_server import FlaskServerManager
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask server manager not available")


class ApiManager(CTkFrame):
    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, fg_color="#e8f4f8", **kwargs)
        self.navigate_callback = navigate_callback
        self.api_status = "stopped"
        self.uptime_start = None
        self.request_count = 0
        self.first_check = True  # Flag to avoid false warning on first check
        
        # Initialize Flask server manager
        if FLASK_AVAILABLE:
            self.flask_server = FlaskServerManager()
        else:
            self.flask_server = None

        # Sidebar
        self._setup_sidebar()

        # Main content
        self._setup_main_content()
        
        # Start status update loop
        self.update_server_status()

    def update_server_status(self):
        """Periodically update server status"""
        if self.flask_server:
            status = self.flask_server.get_status()
            if status["running"]:
                self.api_status = "running"
                uptime = status["uptime"]
                hours = uptime // 3600
                minutes = (uptime % 3600) // 60
                self.stat_widgets[0].configure(text=f"{hours}h {minutes}m")
                
                if self.status_indicator.cget("fg_color") != "#10b981":
                    self.status_indicator.configure(fg_color="#10b981")
                    self.status_text.configure(text="● Running")
            else:
                # Only show warning if server was previously running
                if self.api_status == "running" and not self.first_check:
                    self.api_status = "stopped"
                    self.status_indicator.configure(fg_color="#ef4444")
                    self.status_text.configure(text="● Stopped")
                    self.add_log("[WARNING] Server stopped unexpectedly")
                    
            self.first_check = False
        
        # Schedule next update
        self.after(1000, self.update_server_status)

    def on_server_output(self, line):
        """Handle output from Flask server"""
        if line:
            self.add_log(f"[SERVER] {line}")

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
            ("☁️  My cloud", "Dashboard", False),
            ("👥  Shared files", "Dashboard", False),
            ("⭐  Favorites", "Dashboard", False),
            ("📁  File Manager", "FileManager", False),
            ("⚙️  API Manager", "ApiManager", True)
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
        """Create API manager content"""
        main = CTkScrollableFrame(self, fg_color="transparent")
        main.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        
        # Enable mouse wheel scrolling for all platforms
        self._enable_mousewheel_scrolling(main)

        # Header with back button
        header = CTkFrame(main, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))

        CTkButton(
            header,
            text="← Back to Dashboard",
            command=lambda: self.navigate_callback("Dashboard"),
            fg_color="transparent",
            hover_color="#f1f5f9",
            text_color="#64748b",
            font=("Arial", 13),
            width=160,
            height=35,
            corner_radius=8,
            anchor="w"
        ).pack(side="left")

        # Title card
        self._setup_title_card(main)

        # Stats cards
        self._setup_stats_cards(main)

        # Two column layout
        columns = CTkFrame(main, fg_color="transparent")
        columns.pack(fill="both", expand=True, pady=(20, 0))

        left_col = CTkFrame(columns, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))

        right_col = CTkFrame(columns, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True)

        # Controls
        self._setup_controls(left_col)

        # Logs and config
        self._setup_logs_section(right_col)

    def _enable_mousewheel_scrolling(self, widget):
        """Enable smooth mouse wheel scrolling for all platforms"""
        def _on_mousewheel(event):
            widget._parent_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _on_mousewheel_linux(event):
            if event.num == 4:
                widget._parent_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                widget._parent_canvas.yview_scroll(1, "units")
        
        def _bind_to_mousewheel(event):
            widget._parent_canvas.bind_all("<MouseWheel>", _on_mousewheel)
            widget._parent_canvas.bind_all("<Button-4>", _on_mousewheel_linux)
            widget._parent_canvas.bind_all("<Button-5>", _on_mousewheel_linux)
        
        def _unbind_from_mousewheel(event):
            widget._parent_canvas.unbind_all("<MouseWheel>")
            widget._parent_canvas.unbind_all("<Button-4>")
            widget._parent_canvas.unbind_all("<Button-5>")
        
        widget.bind("<Enter>", _bind_to_mousewheel)
        widget.bind("<Leave>", _unbind_from_mousewheel)

    def _setup_title_card(self, parent):
        """Title section with status"""
        title_card = CTkFrame(parent, fg_color="white", corner_radius=15)
        title_card.pack(fill="x", pady=(0, 20))

        title_content = CTkFrame(title_card, fg_color="transparent")
        title_content.pack(fill="both", padx=30, pady=25)

        # Icon and title
        title_header = CTkFrame(title_content, fg_color="transparent")
        title_header.pack(fill="x")

        icon_bg = CTkFrame(title_header, fg_color="#8b5cf6", width=60, height=60, corner_radius=15)
        icon_bg.pack(side="left", padx=(0, 15))
        icon_bg.pack_propagate(False)
        CTkLabel(icon_bg, text="⚙️", font=("Arial", 28)).pack(expand=True)

        title_text = CTkFrame(title_header, fg_color="transparent")
        title_text.pack(side="left", fill="both", expand=True)

        CTkLabel(
            title_text,
            text="Flask API Manager",
            font=("Arial", 26, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x")

        CTkLabel(
            title_text,
            text="Control and monitor your Flask API server",
            font=("Arial", 13),
            text_color="#64748b",
            anchor="w"
        ).pack(fill="x")

        # Status indicator
        self.status_indicator = CTkFrame(title_header, fg_color="#ef4444", corner_radius=20, height=36)
        self.status_indicator.pack(side="right")
        self.status_indicator.pack_propagate(False)
        
        self.status_text = CTkLabel(
            self.status_indicator,
            text="● Stopped",
            font=("Arial", 12, "bold"),
            text_color="white"
        )
        self.status_text.pack(padx=20, pady=8)

    def _setup_stats_cards(self, parent):
        """API statistics cards"""
        stats_frame = CTkFrame(parent, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 20))

        self.stats_data = [
            {"label": "Uptime", "value": "0h 0m", "icon": "⏱️", "color": "#3b82f6"},
            {"label": "Port", "value": "5000", "icon": "🔌", "color": "#10b981"},
            {"label": "Host", "value": "localhost", "icon": "🌐", "color": "#f59e0b"},
            {"label": "Status", "value": "Stopped", "icon": "⚠️", "color": "#ef4444"},
        ]

        self.stat_widgets = []

        for i, stat in enumerate(self.stats_data):
            card = CTkFrame(stats_frame, fg_color="white", corner_radius=12)
            card.grid(row=0, column=i, padx=6, sticky="nsew")

            card_content = CTkFrame(card, fg_color="transparent")
            card_content.pack(fill="both", padx=20, pady=18)

            # Icon
            icon_bg = CTkFrame(card_content, fg_color=stat["color"], width=42, height=42, corner_radius=10)
            icon_bg.pack(anchor="w")
            icon_bg.pack_propagate(False)
            CTkLabel(icon_bg, text=stat["icon"], font=("Arial", 18)).pack(expand=True)

            # Value
            value_label = CTkLabel(
                card_content,
                text=stat["value"],
                font=("Arial", 22, "bold"),
                text_color="#1e293b",
                anchor="w"
            )
            value_label.pack(fill="x", pady=(10, 2))

            # Label
            CTkLabel(
                card_content,
                text=stat["label"],
                font=("Arial", 11),
                text_color="#64748b",
                anchor="w"
            ).pack(fill="x")

            self.stat_widgets.append(value_label)

        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

    def _setup_controls(self, parent):
        """API control section"""
        CTkLabel(
            parent,
            text="API Controls",
            font=("Arial", 18, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))

        controls_card = CTkFrame(parent, fg_color="white", corner_radius=15)
        controls_card.pack(fill="both", expand=True)

        controls_content = CTkFrame(controls_card, fg_color="transparent")
        controls_content.pack(fill="both", padx=25, pady=25)

        # Control buttons
        buttons = [
            ("▶  Launch API", "#10b981", "Start the Flask server", self.launch_api),
            ("■  Stop API", "#f59e0b", "Gracefully stop the server", self.stop_api),
            ("✕  Kill API", "#ef4444", "Force terminate the server", self.kill_api),
            ("🔄  Restart API", "#3b82f6", "Restart the Flask service", self.restart_api),
        ]

        for text, color, desc, cmd in buttons:
            btn_container = CTkFrame(controls_content, fg_color="transparent")
            btn_container.pack(fill="x", pady=6)

            btn = CTkButton(
                btn_container,
                text=text,
                command=cmd,
                height=50,
                corner_radius=10,
                fg_color=color,
                hover_color=self._darken_color(color),
                font=("Arial", 14, "bold")
            )
            btn.pack(fill="x")

            CTkLabel(
                btn_container,
                text=desc,
                font=("Arial", 10),
                text_color="#94a3b8",
                anchor="w"
            ).pack(fill="x", pady=(4, 0))

        # Configuration section
        CTkLabel(
            controls_content,
            text="Configuration",
            font=("Arial", 15, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(25, 15))

        # Port configuration
        port_frame = CTkFrame(controls_content, fg_color="#f8fafc", corner_radius=10)
        port_frame.pack(fill="x", pady=6)

        port_content = CTkFrame(port_frame, fg_color="transparent")
        port_content.pack(fill="both", padx=15, pady=15)

        CTkLabel(
            port_content,
            text="Server Port",
            font=("Arial", 12, "bold"),
            text_color="#475569",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))

        self.port_entry = CTkEntry(
            port_content,
            placeholder_text="5000",
            height=38,
            corner_radius=8,
            border_width=2,
            border_color="#e2e8f0",
            font=("Arial", 13)
        )
        self.port_entry.insert(0, "5000")
        self.port_entry.pack(fill="x")

        # Host configuration
        host_frame = CTkFrame(controls_content, fg_color="#f8fafc", corner_radius=10)
        host_frame.pack(fill="x", pady=6)

        host_content = CTkFrame(host_frame, fg_color="transparent")
        host_content.pack(fill="both", padx=15, pady=15)

        CTkLabel(
            host_content,
            text="Host Address",
            font=("Arial", 12, "bold"),
            text_color="#475569",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))

        self.host_entry = CTkEntry(
            host_content,
            placeholder_text="localhost",
            height=38,
            corner_radius=8,
            border_width=2,
            border_color="#e2e8f0",
            font=("Arial", 13)
        )
        self.host_entry.insert(0, "localhost")
        self.host_entry.pack(fill="x")

        # Flask app path
        app_frame = CTkFrame(controls_content, fg_color="#f8fafc", corner_radius=10)
        app_frame.pack(fill="x", pady=6)

        app_content = CTkFrame(app_frame, fg_color="transparent")
        app_content.pack(fill="both", padx=15, pady=15)

        CTkLabel(
            app_content,
            text="Flask App Path",
            font=("Arial", 12, "bold"),
            text_color="#475569",
            anchor="w"
        ).pack(fill="x", pady=(0, 8))

        self.app_path_entry = CTkEntry(
            app_content,
            placeholder_text="flask_app.py",
            height=38,
            corner_radius=8,
            border_width=2,
            border_color="#e2e8f0",
            font=("Arial", 13)
        )
        self.app_path_entry.insert(0, "flask_app.py")
        self.app_path_entry.pack(fill="x")

    def _setup_logs_section(self, parent):
        """Logs and monitoring section"""
        CTkLabel(
            parent,
            text="Activity Logs",
            font=("Arial", 18, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))

        logs_card = CTkFrame(parent, fg_color="white", corner_radius=15)
        logs_card.pack(fill="both", expand=True, pady=(0, 20))

        logs_content = CTkFrame(logs_card, fg_color="transparent")
        logs_content.pack(fill="both", padx=25, pady=25)

        # Logs header with clear button
        logs_header = CTkFrame(logs_content, fg_color="transparent")
        logs_header.pack(fill="x", pady=(0, 10))

        CTkLabel(
            logs_header,
            text="Server Logs",
            font=("Arial", 14, "bold"),
            text_color="#1e293b"
        ).pack(side="left")

        CTkButton(
            logs_header,
            text="Clear",
            width=70,
            height=28,
            corner_radius=6,
            fg_color="#f1f5f9",
            text_color="#64748b",
            hover_color="#e2e8f0",
            font=("Arial", 11),
            command=self.clear_logs
        ).pack(side="right")

        # Logs display
        self.logs_frame = CTkTextbox(
            logs_content,
            fg_color="#1e293b",
            corner_radius=10,
            height=250,
            font=("Courier", 11),
            text_color="#94a3b8",
            wrap="word"
        )
        self.logs_frame.pack(fill="both", expand=True)
        self.logs_frame.insert("1.0", "[INFO] Flask API Manager initialized\n[INFO] Ready to start server\n")
        self.logs_frame.configure(state="disabled")

        # Endpoints section
        CTkLabel(
            parent,
            text="API Endpoints",
            font=("Arial", 18, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(10, 15))

        endpoints_card = CTkFrame(parent, fg_color="white", corner_radius=15)
        endpoints_card.pack(fill="x")

        endpoints = [
            ("/api/v1/users", "GET", "#10b981"),
            ("/api/v1/data", "POST", "#3b82f6"),
            ("/api/v1/status", "GET", "#f59e0b"),
            ("/api/v1/delete", "DELETE", "#ef4444"),
        ]

        for endpoint, method, color in endpoints:
            endpoint_item = CTkFrame(endpoints_card, fg_color="#f8fafc", corner_radius=8, height=55)
            endpoint_item.pack(fill="x", padx=20, pady=6)
            endpoint_item.pack_propagate(False)

            endpoint_content = CTkFrame(endpoint_item, fg_color="transparent")
            endpoint_content.pack(fill="both", padx=15, pady=12)

            # Method badge
            method_badge = CTkFrame(endpoint_content, fg_color=color, corner_radius=6, width=60, height=26)
            method_badge.pack(side="left", padx=(0, 12))
            method_badge.pack_propagate(False)
            
            CTkLabel(
                method_badge,
                text=method,
                font=("Arial", 10, "bold"),
                text_color="white"
            ).pack(expand=True)

            # Endpoint path
            CTkLabel(
                endpoint_content,
                text=endpoint,
                font=("Courier", 12, "bold"),
                text_color="#1e293b",
                anchor="w"
            ).pack(side="left", fill="x", expand=True)

            # Test button
            CTkButton(
                endpoint_content,
                text="Test",
                width=60,
                height=26,
                corner_radius=6,
                fg_color="#f1f5f9",
                text_color="#64748b",
                hover_color="#e2e8f0",
                font=("Arial", 11),
                command=lambda e=endpoint: self.test_endpoint(e)
            ).pack(side="right")

    def test_endpoint(self, endpoint):
        """Test an API endpoint"""
        if not self.flask_server or not self.flask_server.is_running:
            self.add_log(f"[ERROR] Cannot test {endpoint} - server is not running")
            return
        
        import webbrowser
        url = f"http://{self.host_entry.get() or 'localhost'}:{self.port_entry.get() or '5000'}{endpoint}"
        webbrowser.open(url)
        self.add_log(f"[INFO] Opening {endpoint} in browser")

    def _darken_color(self, color):
        """Darken hex color for hover effect"""
        color_map = {
            "#10b981": "#059669",
            "#ef4444": "#dc2626",
            "#dc2626": "#b91c1c",
            "#f59e0b": "#d97706",
            "#3b82f6": "#2563eb",
        }
        return color_map.get(color, color)

    def add_log(self, message):
        """Add log message"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.logs_frame.configure(state="normal")
        self.logs_frame.insert("end", f"[{timestamp}] {message}\n")
        self.logs_frame.see("end")
        self.logs_frame.configure(state="disabled")

    def clear_logs(self):
        """Clear all logs"""
        self.logs_frame.configure(state="normal")
        self.logs_frame.delete("1.0", "end")
        self.logs_frame.insert("1.0", "[INFO] Logs cleared\n")
        self.logs_frame.configure(state="disabled")

    def launch_api(self):
        """Launch Flask API server"""
        if not FLASK_AVAILABLE or not self.flask_server:
            self.add_log("[ERROR] Flask server manager not available")
            return
        
        host = self.host_entry.get() or "localhost"
        port = self.port_entry.get() or "5000"
        app_path = self.app_path_entry.get() or "flask_app.py"
        
        # Convert to absolute path
        if not os.path.isabs(app_path):
            app_path = os.path.join(os.getcwd(), app_path)
        
        self.add_log(f"[INFO] Starting Flask server on {host}:{port}...")
        self.add_log(f"[INFO] Flask app: {app_path}")
        
        success, message = self.flask_server.start_server(host, int(port), app_path)
        
        if success:
            self.api_status = "running"
            self.uptime_start = datetime.datetime.now()
            self.status_indicator.configure(fg_color="#10b981")
            self.status_text.configure(text="● Running")
            self.add_log(f"[SUCCESS] {message}")
            self.stat_widgets[1].configure(text=port)
            self.stat_widgets[2].configure(text=host)
            self.stat_widgets[3].configure(text="Running")
            
            # Start reading output in background
            if self.flask_server.process:
                self.flask_server.read_output(callback=self.on_server_output)
        else:
            self.add_log(f"[ERROR] {message}")

    def stop_api(self):
        """Stop Flask API gracefully"""
        if not FLASK_AVAILABLE or not self.flask_server:
            self.add_log("[ERROR] Flask server manager not available")
            return
        
        self.add_log("[INFO] Stopping Flask server...")
        success, message = self.flask_server.stop_server()
        
        if success:
            self.api_status = "stopped"
            self.uptime_start = None
            self.status_indicator.configure(fg_color="#ef4444")
            self.status_text.configure(text="● Stopped")
            self.add_log(f"[SUCCESS] {message}")
            self.stat_widgets[0].configure(text="0h 0m")
            self.stat_widgets[3].configure(text="Stopped")
        else:
            self.add_log(f"[ERROR] {message}")

    def kill_api(self):
        """Force kill Flask API"""
        if not FLASK_AVAILABLE or not self.flask_server:
            self.add_log("[ERROR] Flask server manager not available")
            return
        
        self.add_log("[WARNING] Force killing Flask server...")
        success, message = self.flask_server.kill_server()
        
        if success:
            self.api_status = "stopped"
            self.uptime_start = None
            self.status_indicator.configure(fg_color="#ef4444")
            self.status_text.configure(text="● Stopped")
            self.add_log(f"[SUCCESS] {message}")
            self.stat_widgets[0].configure(text="0h 0m")
            self.stat_widgets[3].configure(text="Stopped")
        else:
            self.add_log(f"[ERROR] {message}")

    def restart_api(self):
        """Restart Flask API server"""
        if not FLASK_AVAILABLE or not self.flask_server:
            self.add_log("[ERROR] Flask server manager not available")
            return
        
        self.add_log("[INFO] Restarting Flask server...")
        
        host = self.host_entry.get() or "localhost"
        port = self.port_entry.get() or "5000"
        app_path = self.app_path_entry.get() or "flask_app.py"
        
        if not os.path.isabs(app_path):
            app_path = os.path.join(os.getcwd(), app_path)
        
        success, message = self.flask_server.restart_server(host, int(port), app_path)
        
        if success:
            self.api_status = "running"
            self.uptime_start = datetime.datetime.now()
            self.status_indicator.configure(fg_color="#10b981")
            self.status_text.configure(text="● Running")
            self.add_log(f"[SUCCESS] {message}")
            self.stat_widgets[1].configure(text=port)
            self.stat_widgets[2].configure(text=host)
            self.stat_widgets[3].configure(text="Running")
            
            # Start reading output
            if self.flask_server.process:
                self.flask_server.read_output(callback=self.on_server_output)
        else:
            self.add_log(f"[ERROR] {message}")

