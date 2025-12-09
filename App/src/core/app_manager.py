# app_manager.py
import customtkinter as ctk
from src.ui.pages.login_page import LoginPage
from src.ui.pages.dashboard import Dashboard
from src.ui.pages.file_manager import FileManager
from src.ui.pages.api_manager import ApiManager

try:
    from tkinterdnd2 import TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("tkinterdnd2 not available - drag and drop will be disabled")


class AppManager(TkinterDnD.Tk if DND_AVAILABLE else ctk.CTk):
    """Main application window that handles page navigation."""

    def __init__(self):
        super().__init__()

        # Configure CustomTkinter settings (these need to be set after super().__init__)
        ctk.set_appearance_mode("dark")  # or "light" or "system"
        ctk.set_default_color_theme("blue")

        self.title("MyApp")
        self.geometry("1100x700")

        # If using TkinterDnD, we need to configure the window for CustomTkinter styling
        if DND_AVAILABLE:
            self._setup_ctk_styling()

        # Create a container frame that stays constant
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # Track pages
        self.pages = {}
        self.current_page = None
        self.is_transitioning = False

        # Start on login
        self.show_page("LoginPage")

    def _setup_ctk_styling(self):
        """Apply CustomTkinter styling to TkinterDnD window"""
        try:
            # Get the theme colors
            if ctk.get_appearance_mode() == "Dark":
                bg_color = "#1a1a1a"
            else:
                bg_color = "#f0f0f0"
            
            self.configure(bg=bg_color)
            
            # Disable compositing effects on Linux for smoother rendering
            try:
                self.attributes('-type', 'dialog')
            except:
                pass
        except Exception as e:
            print(f"Could not apply CTk styling: {e}")

    def show_page(self, page_name: str):
        """Switch between app pages with optimized transition for Linux."""
        # Prevent multiple transitions at once
        if self.is_transitioning:
            return
        
        # Create new page if it doesn't exist
        if page_name not in self.pages:
            self.pages[page_name] = self._create_page(page_name)
        
        new_page = self.pages[page_name]
        
        # If same page, do nothing
        if self.current_page == new_page:
            return
        
        self.is_transitioning = True
        
        # Pre-render the new page off-screen to prevent flickering
        new_page.place(x=0, y=self.winfo_height(), relwidth=1, relheight=1)
        self.update_idletasks()
        
        # If there's a current page, transition
        if self.current_page:
            self._slide_transition(self.current_page, new_page)
        else:
            # First page, just show it
            new_page.place_forget()
            new_page.pack(fill="both", expand=True)
            self.current_page = new_page
            self.is_transitioning = False

    def _slide_transition(self, old_page, new_page):
        """Optimized slide transition for Linux"""
        steps = 8  # Fewer steps for better Linux performance
        delay = 20  # Slightly longer delay for Linux
        height = self.winfo_height()
        
        def animate_step(step):
            if step <= steps:
                progress = step / steps
                
                # Smooth easing function (ease-out)
                eased_progress = 1 - (1 - progress) ** 2
                
                # Old page moves up
                old_y = int(-height * eased_progress)
                old_page.place(x=0, y=old_y, relwidth=1, relheight=1)
                
                # New page moves up from bottom
                new_y = int(height * (1 - eased_progress))
                new_page.place(x=0, y=new_y, relwidth=1, relheight=1)
                
                # Force immediate update for Linux
                self.update_idletasks()
                
                self.after(delay, lambda: animate_step(step + 1))
            else:
                # Animation complete
                old_page.place_forget()
                old_page.pack_forget()
                
                new_page.place_forget()
                new_page.pack(fill="both", expand=True)
                
                self.current_page = new_page
                self.is_transitioning = False
        
        # Start animation with both pages in position
        old_page.place(x=0, y=0, relwidth=1, relheight=1)
        animate_step(1)

    def _create_page(self, page_name: str):
        """Factory for creating pages with navigation callback."""
        pages_map = {
            "LoginPage": LoginPage,
            "Dashboard": Dashboard,
            "FileManager": FileManager,
            "ApiManager": ApiManager,
        }
        page_class = pages_map.get(page_name)
        if not page_class:
            raise ValueError(f"Page '{page_name}' not found.")
        
        # Create page inside the container
        page = page_class(self.container, navigate_callback=self.show_page)
        
        # Pre-configure page for better performance on Linux
        page.pack_forget()  # Don't show it yet
        
        return page
