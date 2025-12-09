# file_manager.py
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os

try:
    from tkinterdnd2 import DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("tkinterdnd2 not available - drag and drop disabled")


class FileManager(ctk.CTkFrame):
    def __init__(self, master, navigate_callback, **kwargs):
        super().__init__(master, fg_color="#e8f4f8", **kwargs)
        self.navigate_callback = navigate_callback
        self._files = []

        # Sidebar
        self._setup_sidebar()
        
        # Main content
        self._setup_main_content()

    def _setup_sidebar(self):
        """Create left sidebar"""
        sidebar = ctk.CTkFrame(self, fg_color="#1e3a8a", width=220, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Profile section
        profile_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        profile_frame.pack(pady=30, padx=20)
        
        # Profile picture placeholder
        profile_pic = ctk.CTkFrame(profile_frame, fg_color="#3b82f6", width=60, height=60, corner_radius=30)
        profile_pic.pack()
        profile_pic.pack_propagate(False)
        ctk.CTkLabel(profile_pic, text="👤", font=("Arial", 24)).pack(expand=True)

        # Navigation buttons
        nav_buttons = [
            ("☁️  My cloud", "Dashboard"),
            ("👥  Shared files", "Dashboard"),
            ("⭐  Favorites", "Dashboard"),
            ("☁️  Upload files", "FileManager")
        ]

        for text, page in nav_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=lambda p=page: self.navigate_callback(p),
                fg_color="transparent",
                hover_color="#2563eb",
                anchor="w",
                height=40,
                font=("Arial", 14)
            )
            btn.pack(fill="x", padx=15, pady=5)

        # Bottom buttons
        ctk.CTkFrame(sidebar, fg_color="transparent", height=20).pack(expand=True)
        
        ctk.CTkButton(
            sidebar,
            text="⚙️  Settings",
            command=lambda: None,
            fg_color="transparent",
            hover_color="#2563eb",
            anchor="w",
            height=40,
            font=("Arial", 14)
        ).pack(fill="x", padx=15, pady=5, side="bottom")
        
        ctk.CTkButton(
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
        """Create main content area"""
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(side="left", fill="both", expand=True, padx=30, pady=30)

        # Search bar
        search_frame = ctk.CTkFrame(main, fg_color="white", height=50, corner_radius=10)
        search_frame.pack(fill="x", pady=(0, 30))
        search_frame.pack_propagate(False)
        
        ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Search",
            fg_color="transparent",
            border_width=0,
            font=("Arial", 14)
        ).pack(fill="both", padx=20, pady=10)

        # Categories header
        ctk.CTkLabel(
            main,
            text="Categories",
            font=("Arial", 20, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))

        # Categories grid
        categories_frame = ctk.CTkFrame(main, fg_color="transparent")
        categories_frame.pack(fill="x", pady=(0, 30))

        categories = [
            ("📷", "Pictures", "480 files", "#8b5cf6"),
            ("📄", "Documents", "190 files", "#06b6d4"),
            ("🎬", "Videos", "30 files", "#ec4899"),
            ("🎵", "Audio", "80 files", "#3b82f6")
        ]

        for i, (icon, name, count, color) in enumerate(categories):
            cat_card = ctk.CTkFrame(
                categories_frame,
                fg_color=color,
                corner_radius=15,
                width=160,
                height=120
            )
            cat_card.grid(row=0, column=i, padx=8, pady=5, sticky="nsew")
            cat_card.pack_propagate(False)
            
            ctk.CTkLabel(
                cat_card,
                text=icon,
                font=("Arial", 32)
            ).pack(pady=(15, 5))
            
            ctk.CTkLabel(
                cat_card,
                text=name,
                font=("Arial", 14, "bold"),
                text_color="white"
            ).pack()
            
            ctk.CTkLabel(
                cat_card,
                text=count,
                font=("Arial", 11),
                text_color="white"
            ).pack()
            
            # Star icon for favorites
            if i == 0:
                star_label = ctk.CTkLabel(cat_card, text="⭐", font=("Arial", 16))
                star_label.place(x=130, y=10)

        # Configure grid weights
        for i in range(4):
            categories_frame.grid_columnconfigure(i, weight=1)

        # Two column layout for Files and Recent files
        columns = ctk.CTkFrame(main, fg_color="transparent")
        columns.pack(fill="both", expand=True)

        left_col = ctk.CTkFrame(columns, fg_color="transparent")
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 15))

        right_col = ctk.CTkFrame(columns, fg_color="transparent")
        right_col.pack(side="right", fill="both", expand=True)

        # Files section (left)
        self._setup_files_section(left_col)

        # Recent files section (right)
        self._setup_recent_files_section(right_col)

    def _setup_files_section(self, parent):
        """Files categories section"""
        ctk.CTkLabel(
            parent,
            text="Files",
            font=("Arial", 18, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))

        files_container = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        files_container.pack(fill="both", expand=True)

        file_cats = [
            ("📁", "Work", "820 files", "#6366f1"),
            ("👤", "Personal", "115 files", "#06b6d4"),
            ("🎓", "School", "65 files", "#ec4899"),
            ("📦", "Archive", "21 files", "#64748b")
        ]

        for icon, name, count, color in file_cats:
            cat_frame = ctk.CTkFrame(files_container, fg_color="transparent", height=80)
            cat_frame.pack(fill="x", padx=20, pady=10)
            cat_frame.pack_propagate(False)

            # Icon
            icon_bg = ctk.CTkFrame(cat_frame, fg_color=color, width=50, height=50, corner_radius=10)
            icon_bg.pack(side="left", padx=(0, 15))
            icon_bg.pack_propagate(False)
            ctk.CTkLabel(icon_bg, text=icon, font=("Arial", 24)).pack(expand=True)

            # Text
            text_frame = ctk.CTkFrame(cat_frame, fg_color="transparent")
            text_frame.pack(side="left", fill="both", expand=True)
            
            ctk.CTkLabel(
                text_frame,
                text=name,
                font=("Arial", 14, "bold"),
                text_color="#1e293b",
                anchor="w"
            ).pack(fill="x")
            
            ctk.CTkLabel(
                text_frame,
                text=count,
                font=("Arial", 12),
                text_color="#64748b",
                anchor="w"
            ).pack(fill="x")

            # Add button
            ctk.CTkButton(
                cat_frame,
                text="+",
                width=40,
                height=40,
                corner_radius=10,
                fg_color="#f1f5f9",
                text_color="#64748b",
                hover_color="#e2e8f0",
                font=("Arial", 20)
            ).pack(side="right")

    def _setup_recent_files_section(self, parent):
        """Recent files and upload section"""
        # Recent files header
        ctk.CTkLabel(
            parent,
            text="Recent files",
            font=("Arial", 18, "bold"),
            text_color="#1e293b",
            anchor="w"
        ).pack(fill="x", pady=(0, 15))

        recent_container = ctk.CTkFrame(parent, fg_color="white", corner_radius=15, height=300)
        recent_container.pack(fill="x", pady=(0, 20))
        recent_container.pack_propagate(False)

        recent_files = [
            ("📷", "IMG_100000", "PNG file", "5 MB", "#8b5cf6"),
            ("🎬", "Startup pitch", "AVI file", "105 MB", "#ec4899"),
            ("🎵", "Freestyle beat", "MP3 file", "21 MB", "#3b82f6"),
            ("📄", "Work proposal", "DOCX file", "500 kb", "#06b6d4")
        ]

        for icon, name, ftype, size, color in recent_files:
            file_frame = ctk.CTkFrame(recent_container, fg_color="transparent", height=60)
            file_frame.pack(fill="x", padx=20, pady=8)
            file_frame.pack_propagate(False)

            # Icon
            icon_bg = ctk.CTkFrame(file_frame, fg_color=color, width=45, height=45, corner_radius=10)
            icon_bg.pack(side="left", padx=(0, 12))
            icon_bg.pack_propagate(False)
            ctk.CTkLabel(icon_bg, text=icon, font=("Arial", 20)).pack(expand=True)

            # File info
            info_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)
            
            ctk.CTkLabel(
                info_frame,
                text=name,
                font=("Arial", 13, "bold"),
                text_color="#1e293b",
                anchor="w"
            ).pack(fill="x")
            
            ctk.CTkLabel(
                info_frame,
                text=f"{ftype}  •  {size}",
                font=("Arial", 11),
                text_color="#94a3b8",
                anchor="w"
            ).pack(fill="x")

            # Action buttons
            btn_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
            btn_frame.pack(side="right")
            
            ctk.CTkButton(
                btn_frame,
                text="🔗",
                width=35,
                height=35,
                corner_radius=8,
                fg_color="#f1f5f9",
                hover_color="#e2e8f0",
                font=("Arial", 14)
            ).pack(side="left", padx=3)
            
            ctk.CTkButton(
                btn_frame,
                text="⋯",
                width=35,
                height=35,
                corner_radius=8,
                fg_color="#f1f5f9",
                hover_color="#e2e8f0",
                font=("Arial", 14)
            ).pack(side="left", padx=3)

        # Add new files section
        self._setup_upload_section(parent)

    def _setup_upload_section(self, parent):
        """Upload/drop zone section"""
        upload_container = ctk.CTkFrame(parent, fg_color="white", corner_radius=15)
        upload_container.pack(fill="both", expand=True)

        # Header with icon
        header_frame = ctk.CTkFrame(upload_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=25, pady=(20, 15))
        
        icon_btn = ctk.CTkFrame(header_frame, fg_color="#3b82f6", width=50, height=50, corner_radius=25)
        icon_btn.pack(side="left", padx=(0, 12))
        icon_btn.pack_propagate(False)
        ctk.CTkLabel(icon_btn, text="⬆", font=("Arial", 24), text_color="white").pack(expand=True)
        
        ctk.CTkLabel(
            header_frame,
            text="Add new files",
            font=("Arial", 16, "bold"),
            text_color="#1e293b"
        ).pack(side="left")

        # Drop zone
        drop_outer = ctk.CTkFrame(upload_container, fg_color="#f1f5f9", corner_radius=12, height=120)
        drop_outer.pack(fill="x", padx=25, pady=(0, 15))
        drop_outer.pack_propagate(False)

        # Canvas for drag and drop
        self.drop_canvas = tk.Canvas(
            drop_outer,
            bg="#f1f5f9",
            highlightthickness=2,
            highlightbackground="#cbd5e1",
            highlightcolor="#3b82f6",
            relief='flat'
        )
        self.drop_canvas.place(relwidth=1, relheight=1)

        # Drop zone content overlay
        drop_content = ctk.CTkFrame(drop_outer, fg_color="transparent")
        drop_content.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(
            drop_content,
            text="Drag and drop files here",
            font=("Arial", 13, "bold"),
            text_color="#64748b"
        ).pack(pady=5)
        
        ctk.CTkLabel(
            drop_content,
            text="or",
            font=("Arial", 11),
            text_color="#94a3b8"
        ).pack(pady=2)
        
        ctk.CTkButton(
            drop_content,
            text="Browse Files",
            command=self.upload_file,
            width=120,
            height=32,
            corner_radius=8,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Arial", 12)
        ).pack(pady=5)

        # Setup drag and drop
        self._setup_drag_drop()

        # Uploaded files list
        self.file_list_frame = ctk.CTkScrollableFrame(
            upload_container,
            fg_color="transparent",
            height=150
        )
        self.file_list_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))
        self.file_items = []

    def _setup_drag_drop(self):
        """Setup drag and drop functionality"""
        if not DND_AVAILABLE:
            return
            
        try:
            self.drop_canvas.drop_target_register(DND_FILES)
            self.drop_canvas.dnd_bind('<<Drop>>', self.on_drop)
            self.drop_canvas.dnd_bind('<<DragEnter>>', self.on_drag_enter)
            self.drop_canvas.dnd_bind('<<DragLeave>>', self.on_drag_leave)
        except Exception as e:
            print(f"Drag & drop setup failed: {e}")

    def on_drag_enter(self, event):
        """Visual feedback on drag enter"""
        self.drop_canvas.configure(bg="#e0e7ff", highlightbackground="#3b82f6")

    def on_drag_leave(self, event):
        """Reset visual on drag leave"""
        self.drop_canvas.configure(bg="#f1f5f9", highlightbackground="#cbd5e1")

    def on_drop(self, event):
        """Handle file drop"""
        try:
            self.drop_canvas.configure(bg="#f1f5f9", highlightbackground="#cbd5e1")
            files = self.drop_canvas.tk.splitlist(event.data)
            for file in files:
                clean_file = file.strip('{}').strip('"')
                if os.path.exists(clean_file):
                    self.add_file(clean_file)
        except Exception as e:
            print(f"Error handling drop: {e}")

    def upload_file(self):
        """Browse and upload file"""
        filepath = filedialog.askopenfilename()
        if filepath:
            self.add_file(filepath)

    def add_file(self, filepath: str):
        """Add file to uploaded list"""
        if filepath not in self._files:
            self._files.append(filepath)
            filename = os.path.basename(filepath)
            file_ext = os.path.splitext(filename)[1].upper().replace('.', '')
            file_size = self._get_file_size(filepath)

            file_frame = ctk.CTkFrame(self.file_list_frame, fg_color="#f8fafc", corner_radius=8, height=50)
            file_frame.pack(fill="x", pady=5)
            file_frame.pack_propagate(False)

            # Icon
            icon_map = {
                'PNG': '📷', 'JPG': '📷', 'JPEG': '📷',
                'PDF': '📄', 'DOCX': '📄', 'DOC': '📄',
                'MP3': '🎵', 'WAV': '🎵',
                'MP4': '🎬', 'AVI': '🎬'
            }
            icon = icon_map.get(file_ext, '📄')
            
            ctk.CTkLabel(file_frame, text=icon, font=("Arial", 18)).pack(side="left", padx=(15, 10))
            
            # File info
            info_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True)
            
            ctk.CTkLabel(
                info_frame,
                text=filename[:30] + "..." if len(filename) > 30 else filename,
                font=("Arial", 12, "bold"),
                text_color="#1e293b",
                anchor="w"
            ).pack(fill="x")
            
            ctk.CTkLabel(
                info_frame,
                text=f"{file_ext} file  •  {file_size}",
                font=("Arial", 10),
                text_color="#64748b",
                anchor="w"
            ).pack(fill="x")
            
            # Remove button
            ctk.CTkButton(
                file_frame,
                text="✕",
                width=30,
                height=30,
                corner_radius=6,
                fg_color="#fee2e2",
                text_color="#dc2626",
                hover_color="#fecaca",
                font=("Arial", 14),
                command=lambda f=file_frame, p=filepath: self.remove_file(f, p)
            ).pack(side="right", padx=10)

            self.file_items.append((file_frame, filepath))

    def _get_file_size(self, filepath):
        """Get human readable file size"""
        try:
            size = os.path.getsize(filepath)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.1f} {unit}"
                size /= 1024.0
            return f"{size:.1f} TB"
        except:
            return "Unknown"

    def remove_file(self, frame, filepath):
        """Remove file from list"""
        frame.destroy()
        if filepath in self._files:
            self._files.remove(filepath)
        self.file_items = [item for item in self.file_items if item[1] != filepath]
