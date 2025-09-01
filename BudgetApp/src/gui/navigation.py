"""
Navigation sidebar with modern styling and smooth interactions.
"""

import customtkinter as ctk
from typing import Callable


class NavigationFrame(ctk.CTkFrame):
    """Modern navigation sidebar with buttons for different sections."""
    
    def __init__(self, parent, navigate_callback: Callable[[str], None]):
        super().__init__(parent, width=250, corner_radius=15)
        
        self.navigate_callback = navigate_callback
        self.navigation_buttons = {}
        self.current_button = None
        
        # Configure grid
        self.grid_rowconfigure(7, weight=1)  # Spacer row
        
        # Create navigation elements
        self.create_header()
        self.create_navigation_buttons()
        self.create_footer()
        
        # Initially disabled until login
        self.enabled = False
    
    def create_header(self):
        """Create the header section with logo/title."""
        # Logo/Title
        self.title_label = ctk.CTkLabel(
            self,
            text="💰 Budget App",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=("gray10", "gray90")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(30, 20), sticky="w")
        
        # Separator
        self.separator = ctk.CTkFrame(self, height=2, fg_color=("gray80", "gray20"))
        self.separator.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
    
    def create_navigation_buttons(self):
        """Create navigation buttons for different sections."""
        
        nav_items = [
            ("📊 Overview", "overview", "View your financial summary"),
            ("💸 Expenses", "expenses", "Track and manage expenses"),
            ("💰 Savings", "savings", "Monitor your savings"),
            ("🎯 Goals", "goals", "Set and track financial goals"),
            ("📈 Reports", "reports", "View detailed reports"),
            ("⚙️ Settings", "settings", "Application settings"),
        ]
        
        for i, (text, page_name, tooltip) in enumerate(nav_items):
            button = ctk.CTkButton(
                self,
                text=text,
                command=lambda p=page_name: self.on_navigate(p),
                font=ctk.CTkFont(size=14, weight="normal"),
                height=45,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray20")
            )
            button.grid(row=i+2, column=0, sticky="ew", padx=15, pady=2)
            
            self.navigation_buttons[page_name] = button
            
            # Add tooltip (simple implementation)
            self.create_tooltip(button, tooltip)
        
        # Set overview as default active
        self.set_active_button("overview")
    
    def create_footer(self):
        """Create footer section with user info and logout."""
        # User info (placeholder for now)
        self.user_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.user_frame.grid(row=8, column=0, sticky="ew", padx=15, pady=10)
        
        self.user_label = ctk.CTkLabel(
            self.user_frame,
            text="👤 Demo User",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60")
        )
        self.user_label.pack(pady=(10, 5))
        
        # Logout button
        self.logout_button = ctk.CTkButton(
            self.user_frame,
            text="🚪 Logout",
            command=self.on_logout,
            font=ctk.CTkFont(size=12),
            height=30,
            fg_color=("red", "darkred"),
            hover_color=("darkred", "red")
        )
        self.logout_button.pack(fill="x")
    
    def create_tooltip(self, widget, text):
        """Simple tooltip implementation."""
        def on_enter(event):
            # Could implement proper tooltip widget here
            pass
        
        def on_leave(event):
            pass
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def on_navigate(self, page_name: str):
        """Handle navigation button clicks."""
        if not self.enabled:
            return
            
        self.set_active_button(page_name)
        self.navigate_callback(page_name)
    
    def set_active_button(self, page_name: str):
        """Set the active navigation button styling."""
        # Reset all buttons to inactive state
        for name, button in self.navigation_buttons.items():
            if name == page_name:
                button.configure(
                    fg_color=("blue", "darkblue"),
                    text_color="white",
                    hover_color=("darkblue", "blue")
                )
                self.current_button = button
            else:
                button.configure(
                    fg_color="transparent",
                    text_color=("gray10", "gray90"),
                    hover_color=("gray80", "gray20")
                )
    
    def set_enabled(self, enabled: bool):
        """Enable or disable navigation."""
        self.enabled = enabled
        
        # Update button states
        state = "normal" if enabled else "disabled"
        for button in self.navigation_buttons.values():
            button.configure(state=state)
        
        self.logout_button.configure(state=state)
        
        # Update visual feedback
        if not enabled:
            for button in self.navigation_buttons.values():
                button.configure(text_color=("gray60", "gray40"))
    
    def on_logout(self):
        """Handle logout button click."""
        if not self.enabled:
            return
        
        # Get parent window and call logout
        main_window = self.master
        if hasattr(main_window, 'logout'):
            main_window.logout()
    
    def update_user_info(self, username: str):
        """Update the displayed user information."""
        self.user_label.configure(text=f"👤 {username}")


class NavigationButton(ctk.CTkButton):
    """Custom navigation button with enhanced styling."""
    
    def __init__(self, parent, text: str, command: Callable, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            font=ctk.CTkFont(size=14),
            height=45,
            anchor="w",
            **kwargs
        )
        
        # Custom styling
        self.configure(
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray20"),
            corner_radius=10
        )
    
    def set_active(self, active: bool):
        """Set button active state."""
        if active:
            self.configure(
                fg_color=("blue", "darkblue"),
                text_color="white",
                hover_color=("darkblue", "blue")
            )
        else:
            self.configure(
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray20")
            )