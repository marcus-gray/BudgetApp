"""
Password reset interface with token-based reset mechanism.
"""

import customtkinter as ctk
from typing import Callable, Optional
from ..components.theme_manager import theme_manager
from ...auth.authentication import auth_service


class PasswordResetDialog(ctk.CTkToplevel):
    """Password reset dialog window."""
    
    def __init__(self, parent, callback: Callable = None):
        super().__init__(parent)
        
        self.callback = callback
        self.current_step = "request"  # "request", "token_input", "new_password"
        self.reset_token = None
        self.reset_user = None
        
        # Configure window
        self.title("Password Reset")
        self.geometry("400x500")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()  # Modal dialog
        
        # Center on parent
        self.center_on_parent(parent)
        
        # Create interface
        self.create_interface()
    
    def center_on_parent(self, parent):
        """Center dialog on parent window."""
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 200
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 250
        self.geometry(f"400x500+{x}+{y}")
    
    def create_interface(self):
        """Create the reset interface."""
        # Main container
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # Content frame (will be updated based on step)
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.main_container,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=350
        )
        self.status_label.pack(pady=10)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=10)
        
        # Show initial step
        self.show_request_step()
    
    def create_header(self):
        """Create header section."""
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Icon
        icon_label = ctk.CTkLabel(
            header_frame,
            text="🔑",
            font=ctk.CTkFont(size=32)
        )
        icon_label.pack(pady=(0, 10))
        
        # Title
        self.title_label = ctk.CTkLabel(
            header_frame,
            text="Reset Password",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack()
        
        # Subtitle
        self.subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Enter your username or email to reset your password",
            font=ctk.CTkFont(size=12),
            text_color=theme_manager.get_color("text_secondary"),
            wraplength=350
        )
        self.subtitle_label.pack(pady=(5, 0))
    
    def clear_content(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def clear_buttons(self):
        """Clear the buttons frame."""
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()
    
    def show_request_step(self):
        """Show the initial password reset request step."""
        self.current_step = "request"
        self.clear_content()
        self.clear_buttons()
        
        # Update header
        self.title_label.configure(text="Reset Password")
        self.subtitle_label.configure(text="Enter your username or email to reset your password")
        
        # Username/Email input
        label = ctk.CTkLabel(
            self.content_frame,
            text="Username or Email",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", pady=(20, 5))
        
        self.username_entry = ctk.CTkEntry(
            self.content_frame,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Enter username or email",
            **theme_manager.get_input_style()
        )
        self.username_entry.pack(fill="x", pady=(0, 20))
        self.username_entry.focus()
        
        # Instructions
        instruction_text = ("We'll generate a secure reset token for your account. "
                          "In a real application, this would be sent to your email.")
        instruction_label = ctk.CTkLabel(
            self.content_frame,
            text=instruction_text,
            font=ctk.CTkFont(size=11),
            text_color=theme_manager.get_color("text_secondary"),
            wraplength=350,
            justify="left"
        )
        instruction_label.pack(pady=(0, 20))
        
        # Buttons
        request_button = ctk.CTkButton(
            self.buttons_frame,
            text="Generate Reset Token",
            command=self.handle_reset_request,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            **theme_manager.get_button_style("primary")
        )
        request_button.pack(side="right", padx=(10, 0))
        
        cancel_button = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            command=self.destroy,
            font=ctk.CTkFont(size=14),
            height=40,
            **theme_manager.get_button_style("secondary")
        )
        cancel_button.pack(side="right")
    
    def show_token_step(self, token: str):
        """Show the token input step."""
        self.current_step = "token_input"
        self.reset_token = token
        self.clear_content()
        self.clear_buttons()
        
        # Update header
        self.title_label.configure(text="Reset Token Generated")
        self.subtitle_label.configure(text="Copy the token below and paste it in the verification field")
        
        # Token display
        token_label = ctk.CTkLabel(
            self.content_frame,
            text="Your Reset Token:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        token_label.pack(fill="x", pady=(20, 5))
        
        # Token text box (read-only)
        token_textbox = ctk.CTkTextbox(
            self.content_frame,
            height=60,
            font=ctk.CTkFont(size=10, family="monospace")
        )
        token_textbox.pack(fill="x", pady=(0, 15))
        token_textbox.insert("1.0", token)
        token_textbox.configure(state="disabled")
        
        # Copy button
        copy_button = ctk.CTkButton(
            self.content_frame,
            text="📋 Copy Token",
            command=lambda: self.copy_to_clipboard(token),
            font=ctk.CTkFont(size=12),
            height=30,
            **theme_manager.get_button_style("secondary")
        )
        copy_button.pack(pady=(0, 15))
        
        # Verification input
        verify_label = ctk.CTkLabel(
            self.content_frame,
            text="Paste Token Here:",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        verify_label.pack(fill="x", pady=(10, 5))
        
        self.token_entry = ctk.CTkEntry(
            self.content_frame,
            font=ctk.CTkFont(size=12, family="monospace"),
            height=40,
            placeholder_text="Paste your reset token here",
            **theme_manager.get_input_style()
        )
        self.token_entry.pack(fill="x", pady=(0, 20))
        
        # Buttons
        verify_button = ctk.CTkButton(
            self.buttons_frame,
            text="Verify Token",
            command=self.handle_token_verification,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            **theme_manager.get_button_style("primary")
        )
        verify_button.pack(side="right", padx=(10, 0))
        
        back_button = ctk.CTkButton(
            self.buttons_frame,
            text="Back",
            command=self.show_request_step,
            font=ctk.CTkFont(size=14),
            height=40,
            **theme_manager.get_button_style("secondary")
        )
        back_button.pack(side="right")
    
    def show_password_step(self):
        """Show the new password input step."""
        self.current_step = "new_password"
        self.clear_content()
        self.clear_buttons()
        
        # Update header
        self.title_label.configure(text="Set New Password")
        self.subtitle_label.configure(text="Enter your new password below")
        
        # New password input
        label1 = ctk.CTkLabel(
            self.content_frame,
            text="New Password",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        label1.pack(fill="x", pady=(20, 5))
        
        self.new_password_entry = ctk.CTkEntry(
            self.content_frame,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Enter new password",
            show="*",
            **theme_manager.get_input_style()
        )
        self.new_password_entry.pack(fill="x", pady=(0, 15))
        
        # Confirm password input
        label2 = ctk.CTkLabel(
            self.content_frame,
            text="Confirm New Password",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        label2.pack(fill="x", pady=(0, 5))
        
        self.confirm_password_entry = ctk.CTkEntry(
            self.content_frame,
            font=ctk.CTkFont(size=14),
            height=40,
            placeholder_text="Confirm new password",
            show="*",
            **theme_manager.get_input_style()
        )
        self.confirm_password_entry.pack(fill="x", pady=(0, 15))
        
        # Password requirements
        requirements_text = ("Password must be at least 8 characters long and contain:\\n"
                           "• At least one uppercase letter\\n"
                           "• At least one lowercase letter\\n"
                           "• At least one number\\n"
                           "• At least one special character")
        
        requirements_label = ctk.CTkLabel(
            self.content_frame,
            text=requirements_text,
            font=ctk.CTkFont(size=10),
            text_color=theme_manager.get_color("text_secondary"),
            wraplength=350,
            justify="left"
        )
        requirements_label.pack(pady=(0, 20))
        
        # Buttons
        reset_button = ctk.CTkButton(
            self.buttons_frame,
            text="Reset Password",
            command=self.handle_password_reset,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            **theme_manager.get_button_style("success")
        )
        reset_button.pack(side="right", padx=(10, 0))
        
        back_button = ctk.CTkButton(
            self.buttons_frame,
            text="Back",
            command=lambda: self.show_token_step(self.reset_token),
            font=ctk.CTkFont(size=14),
            height=40,
            **theme_manager.get_button_style("secondary")
        )
        back_button.pack(side="right")
    
    def handle_reset_request(self):
        """Handle password reset request."""
        username_or_email = self.username_entry.get().strip()
        
        if not username_or_email:
            self.show_status("Please enter your username or email", "error")
            return
        
        # Clear previous status
        self.clear_status()
        
        # Generate reset token
        success, message, token = auth_service.generate_password_reset_token(username_or_email)
        
        if success and token:
            self.show_status("Reset token generated successfully!", "success")
            self.after(1000, lambda: self.show_token_step(token))
        else:
            self.show_status(message, "error")
    
    def handle_token_verification(self):
        """Handle token verification."""
        entered_token = self.token_entry.get().strip()
        
        if not entered_token:
            self.show_status("Please paste your reset token", "error")
            return
        
        # Clear previous status
        self.clear_status()
        
        # Validate token
        valid, message, user = auth_service.validate_reset_token(entered_token)
        
        if valid and user:
            self.reset_user = user
            self.reset_token = entered_token
            self.show_status("Token verified successfully!", "success")
            self.after(1000, self.show_password_step)
        else:
            self.show_status(message, "error")
    
    def handle_password_reset(self):
        """Handle the actual password reset."""
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not new_password or not confirm_password:
            self.show_status("Please fill in both password fields", "error")
            return
        
        # Clear previous status
        self.clear_status()
        
        # Reset password
        success, message = auth_service.reset_password_with_token(
            self.reset_token, new_password, confirm_password
        )
        
        if success:
            self.show_status("Password reset successfully!", "success")
            self.after(2000, self.close_with_success)
        else:
            self.show_status(message, "error")
    
    def copy_to_clipboard(self, text: str):
        """Copy text to clipboard."""
        try:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.show_status("Token copied to clipboard!", "success")
        except Exception:
            self.show_status("Could not copy to clipboard", "error")
    
    def show_status(self, message: str, status_type: str = "info"):
        """Show a status message."""
        colors = theme_manager.get_status_colors()
        color = colors.get(status_type, colors["info"])
        self.status_label.configure(text=message, text_color=color)
        
        # Auto-clear success messages
        if status_type == "success":
            self.after(3000, self.clear_status)
    
    def clear_status(self):
        """Clear the status message."""
        self.status_label.configure(text="")
    
    def close_with_success(self):
        """Close dialog and notify parent of success."""
        if self.callback:
            self.callback(True)
        self.destroy()


class LockoutBypassDialog(ctk.CTkToplevel):
    """Emergency lockout bypass dialog for administrative use."""
    
    def __init__(self, parent, callback: Callable = None):
        super().__init__(parent)
        
        self.callback = callback
        
        # Configure window
        self.title("Emergency Account Unlock")
        self.geometry("350x300")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.center_on_parent(parent)
        
        # Create interface
        self.create_interface()
    
    def center_on_parent(self, parent):
        """Center dialog on parent window."""
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 175
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 150
        self.geometry(f"350x300+{x}+{y}")
    
    def create_interface(self):
        """Create the bypass interface."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_label = ctk.CTkLabel(
            main_frame,
            text="🚨 Emergency Unlock",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        header_label.pack(pady=(0, 20))
        
        # Warning
        warning_label = ctk.CTkLabel(
            main_frame,
            text="This will bypass account lockout protection. Use only in emergencies.",
            font=ctk.CTkFont(size=11),
            text_color=theme_manager.get_color("warning"),
            wraplength=300
        )
        warning_label.pack(pady=(0, 20))
        
        # Username input
        label = ctk.CTkLabel(
            main_frame,
            text="Username or Email:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        label.pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            main_frame,
            font=ctk.CTkFont(size=14),
            height=35,
            **theme_manager.get_input_style()
        )
        self.username_entry.pack(fill="x", pady=(0, 20))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=300
        )
        self.status_label.pack(pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        unlock_button = ctk.CTkButton(
            button_frame,
            text="Generate Unlock Token",
            command=self.generate_unlock_token,
            **theme_manager.get_button_style("warning")
        )
        unlock_button.pack(side="right", padx=(10, 0))
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.destroy,
            **theme_manager.get_button_style("secondary")
        )
        cancel_button.pack(side="right")
    
    def generate_unlock_token(self):
        """Generate an emergency unlock token."""
        username = self.username_entry.get().strip()
        
        if not username:
            self.show_status("Please enter username or email", "error")
            return
        
        success, message, token = auth_service.generate_lockout_bypass_token(
            username, "Emergency unlock via GUI"
        )
        
        if success and token:
            self.show_unlock_token(token)
        else:
            self.show_status(message, "error")
    
    def show_unlock_token(self, token: str):
        """Show the generated unlock token."""
        # Clear existing content
        for widget in self.winfo_children():
            widget.destroy()
        
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(
            main_frame,
            text="Unlock Token Generated",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Token display
        token_textbox = ctk.CTkTextbox(main_frame, height=60, font=ctk.CTkFont(size=10, family="monospace"))
        token_textbox.pack(fill="x", pady=(0, 10))
        token_textbox.insert("1.0", token)
        token_textbox.configure(state="disabled")
        
        # Use token button
        use_button = ctk.CTkButton(
            main_frame,
            text="Use This Token to Unlock",
            command=lambda: self.use_unlock_token(token),
            **theme_manager.get_button_style("primary")
        )
        use_button.pack(pady=10)
        
        self.status_label = ctk.CTkLabel(main_frame, text="", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=10)
    
    def use_unlock_token(self, token: str):
        """Use the unlock token."""
        success, message = auth_service.use_lockout_bypass_token(token)
        
        if success:
            self.show_status("Account unlocked successfully!", "success")
            if self.callback:
                self.callback(True)
            self.after(2000, self.destroy)
        else:
            self.show_status(message, "error")
    
    def show_status(self, message: str, status_type: str = "info"):
        """Show status message."""
        colors = theme_manager.get_status_colors()
        color = colors.get(status_type, colors["info"])
        self.status_label.configure(text=message, text_color=color)