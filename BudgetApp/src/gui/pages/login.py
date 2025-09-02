"""
Login and registration page with modern design.
"""

import customtkinter as ctk
from typing import Callable, Optional
from ..components.theme_manager import theme_manager
from ...auth.authentication import auth_service
from ...database.models import User


class LoginFrame(ctk.CTkFrame):
    """Modern login and registration interface."""
    
    def __init__(self, parent, login_callback: Callable[[User], None]):
        super().__init__(parent)
        
        self.login_callback = login_callback
        self.current_mode = "login"  # "login" or "register"
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.create_login_interface()
    
    def create_login_interface(self):
        """Create the login/registration interface."""
        # Main container
        self.main_container = ctk.CTkFrame(self, width=400, height=500)
        self.main_container.grid(row=0, column=0, padx=20, pady=20)
        self.main_container.grid_propagate(False)
        
        # Header
        self.create_header()
        
        # Form container
        self.form_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.form_container.grid(row=1, column=0, sticky="ew", padx=30, pady=20)
        self.form_container.grid_columnconfigure(0, weight=1)
        
        # Create login form initially
        self.create_login_form()
        
        # Mode toggle
        self.create_mode_toggle()
        
        # Status message
        self.status_label = ctk.CTkLabel(
            self.main_container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=theme_manager.get_status_colors()["error"]
        )
        self.status_label.grid(row=3, column=0, pady=10)
    
    def create_header(self):
        """Create the header section."""
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 10))
        
        # Logo/Icon
        logo_label = ctk.CTkLabel(
            header_frame,
            text="💰",
            font=ctk.CTkFont(size=48)
        )
        logo_label.pack(pady=(0, 10))
        
        # Title
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Welcome to Budget App",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack()
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Sign in to manage your finances",
            font=ctk.CTkFont(size=14),
            text_color=theme_manager.get_color("text_secondary")
        )
        self.subtitle_label.pack(pady=(5, 0))
    
    def create_login_form(self):
        """Create the login form."""
        # Clear existing form
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        # Username/Email field
        self.username_entry = self.create_input_field(
            self.form_container,
            "Username or Email",
            row=0
        )
        
        # Password field
        self.password_entry = self.create_input_field(
            self.form_container,
            "Password",
            row=1,
            show="*"
        )
        
        # Login button
        login_button = ctk.CTkButton(
            self.form_container,
            text="Sign In",
            command=self.handle_login,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            **theme_manager.get_button_style("primary")
        )
        login_button.grid(row=2, column=0, sticky="ew", pady=20)
        
        # Forgot password link
        forgot_label = ctk.CTkLabel(
            self.form_container,
            text="Forgot your password?",
            font=ctk.CTkFont(size=12),
            text_color=theme_manager.get_color("primary"),
            cursor="hand2"
        )
        forgot_label.grid(row=3, column=0, pady=5)
        forgot_label.bind("<Button-1>", lambda e: self.show_password_reset_dialog())
    
    def create_register_form(self):
        """Create the registration form."""
        # Clear existing form
        for widget in self.form_container.winfo_children():
            widget.destroy()
        
        # Username field
        self.username_entry = self.create_input_field(
            self.form_container,
            "Username",
            row=0
        )
        
        # Email field
        self.email_entry = self.create_input_field(
            self.form_container,
            "Email",
            row=1
        )
        
        # Password field
        self.password_entry = self.create_input_field(
            self.form_container,
            "Password",
            row=2,
            show="*"
        )
        
        # Confirm password field
        self.confirm_password_entry = self.create_input_field(
            self.form_container,
            "Confirm Password",
            row=3,
            show="*"
        )
        
        # Register button
        register_button = ctk.CTkButton(
            self.form_container,
            text="Create Account",
            command=self.handle_register,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            **theme_manager.get_button_style("success")
        )
        register_button.grid(row=4, column=0, sticky="ew", pady=20)
    
    def create_input_field(self, parent, placeholder: str, row: int, show: str = None) -> ctk.CTkEntry:
        """Create a styled input field."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text=placeholder,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        label.grid(row=row*2, column=0, sticky="w", pady=(10, 5))
        
        # Entry
        entry = ctk.CTkEntry(
            parent,
            placeholder_text=placeholder,
            font=ctk.CTkFont(size=14),
            height=40,
            show=show,
            **theme_manager.get_input_style()
        )
        entry.grid(row=row*2+1, column=0, sticky="ew", pady=(0, 5))
        
        return entry
    
    def create_mode_toggle(self):
        """Create the toggle between login and register modes."""
        toggle_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        toggle_frame.grid(row=2, column=0, pady=20)
        
        self.toggle_text = ctk.CTkLabel(
            toggle_frame,
            text="Don't have an account?",
            font=ctk.CTkFont(size=12)
        )
        self.toggle_text.pack(side="left", padx=(0, 5))
        
        self.toggle_button = ctk.CTkLabel(
            toggle_frame,
            text="Sign Up",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=theme_manager.get_color("primary"),
            cursor="hand2"
        )
        self.toggle_button.pack(side="left")
        self.toggle_button.bind("<Button-1>", lambda e: self.toggle_mode())
    
    def toggle_mode(self):
        """Toggle between login and registration modes."""
        if self.current_mode == "login":
            self.current_mode = "register"
            self.title_label.configure(text="Create Account")
            self.subtitle_label.configure(text="Join Budget App to start tracking your finances")
            self.create_register_form()
            self.toggle_text.configure(text="Already have an account?")
            self.toggle_button.configure(text="Sign In")
        else:
            self.current_mode = "login"
            self.title_label.configure(text="Welcome Back")
            self.subtitle_label.configure(text="Sign in to manage your finances")
            self.create_login_form()
            self.toggle_text.configure(text="Don't have an account?")
            self.toggle_button.configure(text="Sign Up")
        
        # Clear status
        self.clear_status()
    
    def handle_login(self):
        """Handle login attempt."""
        username_or_email = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        # Clear previous status
        self.clear_status()
        
        # Validate inputs
        if not username_or_email:
            self.show_status("Please enter your username or email", "error")
            return
        
        if not password:
            self.show_status("Please enter your password", "error")
            return
        
        # Attempt login
        success, message, user = auth_service.login_user(username_or_email, password)
        
        if success:
            self.show_status(message, "success")
            self.after(500, lambda: self.login_callback(user))  # Small delay for user feedback
        else:
            self.show_status(message, "error")
            
            # Show emergency unlock option for locked accounts
            if "Account locked" in message and "emergency" not in message.lower():
                self.show_emergency_unlock_option()
    
    def handle_register(self):
        """Handle registration attempt."""
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # Clear previous status
        self.clear_status()
        
        # Basic validation
        if not all([username, email, password, confirm_password]):
            self.show_status("Please fill in all fields", "error")
            return
        
        # Attempt registration
        success, message, user = auth_service.register_user(username, email, password, confirm_password)
        
        if success:
            self.show_status(message, "success")
            self.after(1000, lambda: self.login_callback(user))  # Delay for user feedback
        else:
            self.show_status(message, "error")
    
    def show_status(self, message: str, status_type: str = "info"):
        """Show a status message."""
        colors = theme_manager.get_status_colors()
        color = colors.get(status_type, colors["info"])
        
        self.status_label.configure(text=message, text_color=color)
    
    def clear_status(self):
        """Clear the status message."""
        self.status_label.configure(text="")
    
    def focus_first_field(self):
        """Focus the first input field."""
        if hasattr(self, 'username_entry'):
            self.username_entry.focus()
    
    def show_password_reset_dialog(self):
        """Show password reset dialog."""
        from .password_reset import PasswordResetDialog
        
        dialog = PasswordResetDialog(self, callback=self.on_password_reset_complete)
    
    def on_password_reset_complete(self, success: bool):
        """Handle password reset completion."""
        if success:
            self.show_status("Password reset successfully! You can now log in with your new password.", "success")
    
    def show_emergency_unlock_option(self):
        """Show emergency unlock option for locked accounts."""
        # Add emergency unlock button
        if hasattr(self, 'emergency_unlock_button'):
            return  # Already showing
        
        self.emergency_unlock_button = ctk.CTkButton(
            self.form_container,
            text="🚨 Emergency Unlock",
            command=self.show_emergency_unlock_dialog,
            font=ctk.CTkFont(size=11),
            height=30,
            **theme_manager.get_button_style("warning")
        )
        
        if self.current_mode == "login":
            self.emergency_unlock_button.grid(row=4, column=0, pady=10)
        
        # Auto-remove after 30 seconds
        self.after(30000, self.hide_emergency_unlock_option)
    
    def hide_emergency_unlock_option(self):
        """Hide emergency unlock option."""
        if hasattr(self, 'emergency_unlock_button'):
            self.emergency_unlock_button.destroy()
            delattr(self, 'emergency_unlock_button')
    
    def show_emergency_unlock_dialog(self):
        """Show emergency unlock dialog."""
        from .password_reset import LockoutBypassDialog
        
        dialog = LockoutBypassDialog(self, callback=self.on_emergency_unlock_complete)
    
    def on_emergency_unlock_complete(self, success: bool):
        """Handle emergency unlock completion."""
        if success:
            self.show_status("Account unlocked successfully! You can now try logging in again.", "success")
            self.hide_emergency_unlock_option()


class DemoLoginButton(ctk.CTkButton):
    """Quick demo login button for development."""
    
    def __init__(self, parent, login_callback: Callable[[User], None]):
        super().__init__(
            parent,
            text="🚀 Demo Login (Development)",
            command=lambda: self.demo_login(login_callback),
            font=ctk.CTkFont(size=12),
            height=30,
            **theme_manager.get_button_style("secondary")
        )
    
    def demo_login(self, login_callback: Callable[[User], None]):
        """Quick demo login for development."""
        from datetime import datetime
        
        demo_user = User(
            id=999,
            username="demo_user",
            email="demo@example.com",
            password_hash="",
            created_at=datetime.now()
        )
        
        login_callback(demo_user)