"""
Main application window with modern CustomTkinter design.
Provides the main interface and navigation system.
"""

import customtkinter as ctk
from typing import Optional, Callable
from .navigation import NavigationFrame
from .components.theme_manager import ThemeManager


class MainWindow(ctk.CTk):
    """Main application window with modern design and navigation."""
    
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Budget App")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Initialize theme
        self.theme_manager = ThemeManager()
        self.theme_manager.apply_theme()
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Current user (will be set after login)
        self.current_user = None
        
        # Content frames
        self.content_frames = {}
        self.current_frame = None
        
        # Create UI components
        self.create_navigation()
        self.create_main_content()
        self.create_status_bar()
        
        # Show login initially
        self.show_login()
    
    def create_navigation(self):
        """Create the navigation sidebar."""
        self.navigation_frame = NavigationFrame(self, self.navigate_to)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def create_main_content(self):
        """Create the main content area."""
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def create_status_bar(self):
        """Create the status bar at the bottom."""
        self.status_frame = ctk.CTkFrame(self, height=30)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0, 10))
        self.status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Theme toggle button
        self.theme_button = ctk.CTkButton(
            self.status_frame,
            text="🌙",
            width=40,
            command=self.toggle_theme,
            font=ctk.CTkFont(size=16)
        )
        self.theme_button.grid(row=0, column=1, padx=10, pady=5)
    
    def navigate_to(self, page_name: str):
        """Navigate to a specific page."""
        # Hide current frame
        if self.current_frame:
            self.current_frame.grid_forget()
        
        # Import and create the requested frame
        frame = self.get_or_create_frame(page_name)
        
        if frame:
            frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.current_frame = frame
            self.update_status(f"Viewing {page_name.title()}")
    
    def get_or_create_frame(self, page_name: str):
        """Get existing frame or create new one."""
        if page_name in self.content_frames:
            return self.content_frames[page_name]
        
        # Import the frame class dynamically
        try:
            if page_name == "overview":
                from .pages.overview import OverviewFrame
                frame = OverviewFrame(self.content_frame, self.current_user)
            elif page_name == "expenses":
                from .pages.expenses import ExpensesFrame
                frame = ExpensesFrame(self.content_frame, self.current_user)
            elif page_name == "savings":
                from .pages.savings import SavingsFrame
                frame = SavingsFrame(self.content_frame, self.current_user)
            elif page_name == "goals":
                from .pages.goals import GoalsFrame
                frame = GoalsFrame(self.content_frame, self.current_user)
            elif page_name == "reports":
                from .pages.reports import ReportsFrame
                frame = ReportsFrame(self.content_frame, self.current_user)
            elif page_name == "settings":
                from .pages.settings import SettingsFrame
                frame = SettingsFrame(self.content_frame, self.current_user)
            else:
                # Default placeholder frame
                frame = self.create_placeholder_frame(page_name)
            
            self.content_frames[page_name] = frame
            return frame
            
        except ImportError:
            # Create placeholder frame if page doesn't exist yet
            return self.create_placeholder_frame(page_name)
    
    def create_placeholder_frame(self, page_name: str):
        """Create a placeholder frame for unimplemented pages."""
        frame = ctk.CTkFrame(self.content_frame)
        
        title_label = ctk.CTkLabel(
            frame,
            text=f"{page_name.title()} Page",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=50)
        
        subtitle_label = ctk.CTkLabel(
            frame,
            text="This page is coming soon!",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack()
        
        return frame
    
    def show_login(self):
        """Show the login screen."""
        try:
            from .pages.login import LoginFrame
            login_frame = LoginFrame(self.content_frame, self.on_login_success)
            login_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            self.current_frame = login_frame
            
            # Hide navigation until logged in
            self.navigation_frame.set_enabled(False)
            self.update_status("Please log in to continue")
            
        except ImportError:
            # Create simple login placeholder
            self.create_login_placeholder()
    
    def create_login_placeholder(self):
        """Create a simple login placeholder."""
        frame = ctk.CTkFrame(self.content_frame)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            frame,
            text="Budget App",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(100, 20))
        
        subtitle_label = ctk.CTkLabel(
            frame,
            text="Login system coming soon...",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack()
        
        # Temporary button to continue without login
        temp_button = ctk.CTkButton(
            frame,
            text="Continue as Guest",
            command=self.temp_login,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        temp_button.pack(pady=30)
        
        self.current_frame = frame
    
    def temp_login(self):
        """Temporary login function for development."""
        # Mock user for development
        from ..database.models import User
        from datetime import datetime
        
        self.current_user = User(
            id=1,
            username="demo_user",
            email="demo@example.com",
            password_hash="",
            created_at=datetime.now()
        )
        
        self.on_login_success(self.current_user)
    
    def on_login_success(self, user):
        """Handle successful login."""
        self.current_user = user
        self.navigation_frame.set_enabled(True)
        self.navigate_to("overview")
        self.update_status(f"Welcome, {user.username}!")
    
    def logout(self):
        """Handle user logout."""
        self.current_user = None
        self.content_frames.clear()  # Clear cached frames
        self.show_login()
    
    def toggle_theme(self):
        """Toggle between light and dark theme."""
        self.theme_manager.toggle_theme()
        # Update button icon
        if self.theme_manager.is_dark_mode():
            self.theme_button.configure(text="☀️")
        else:
            self.theme_button.configure(text="🌙")
    
    def update_status(self, message: str):
        """Update the status bar message."""
        self.status_label.configure(text=message)
    
    def run(self):
        """Start the application."""
        self.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()