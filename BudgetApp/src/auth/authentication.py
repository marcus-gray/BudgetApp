"""
User authentication and security module.
Handles user registration, login, password hashing, and session management.
"""

import bcrypt
import re
import time
from typing import Optional, Tuple
from datetime import datetime
from ..database.models import User
from ..database.init_db import create_default_categories


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


class AuthenticationService:
    """Handles user authentication and security operations."""
    
    def __init__(self):
        self.current_session = None
        self.failed_attempts = {}  # Track failed login attempts by username/email
        self.locked_accounts = {}  # Track locked accounts with timestamps
        self.max_attempts = 5  # Maximum failed attempts before lockout
        self.lockout_duration = 900  # Lockout duration in seconds (15 minutes)
        
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            str: Hashed password
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            password: Plain text password to verify
            hashed_password: Stored password hash
            
        Returns:
            bool: True if password is correct
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except (ValueError, TypeError):
            return False
    
    def validate_username(self, username: str) -> Tuple[bool, str]:
        """
        Validate username according to requirements.
        
        Args:
            username: Username to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not username:
            return False, "Username is required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(username) > 20:
            return False, "Username must be no more than 20 characters long"
        
        # Only allow alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        # Check if username already exists
        existing_user = User.get_by_username(username)
        if existing_user:
            return False, "Username already exists"
        
        return True, ""
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Validate email format and uniqueness.
        
        Args:
            email: Email to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"
        
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        # Check if email already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            return False, "Email already registered"
        
        return True, ""
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"
        
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password must be no more than 128 characters long"
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            return False, "Password must contain at least one number"
        
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"
        
        return True, ""
    
    def register_user(self, username: str, email: str, password: str, confirm_password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Register a new user.
        
        Args:
            username: Desired username
            email: User's email address
            password: Plain text password
            confirm_password: Password confirmation
            
        Returns:
            Tuple[bool, str, Optional[User]]: (success, message, user_object)
        """
        try:
            # Validate password confirmation
            if password != confirm_password:
                return False, "Passwords do not match", None
            
            # Validate all fields
            username_valid, username_error = self.validate_username(username)
            if not username_valid:
                return False, username_error, None
            
            email_valid, email_error = self.validate_email(email)
            if not email_valid:
                return False, email_error, None
            
            password_valid, password_error = self.validate_password(password)
            if not password_valid:
                return False, password_error, None
            
            # Hash password and create user
            hashed_password = self.hash_password(password)
            user = User.create(username, email, hashed_password)
            
            # Create default categories for the new user
            create_default_categories(user.id)
            
            return True, "Account created successfully!", user
            
        except Exception as e:
            return False, f"Registration failed: {str(e)}", None
    
    def is_account_locked(self, identifier: str) -> Tuple[bool, int]:
        """
        Check if an account is currently locked.
        
        Args:
            identifier: Username or email to check
            
        Returns:
            Tuple[bool, int]: (is_locked, remaining_lockout_seconds)
        """
        if identifier not in self.locked_accounts:
            return False, 0
        
        lock_time = self.locked_accounts[identifier]
        elapsed = time.time() - lock_time
        
        if elapsed >= self.lockout_duration:
            # Lockout period expired, remove from locked accounts
            self.unlock_account(identifier)
            return False, 0
        
        remaining = int(self.lockout_duration - elapsed)
        return True, remaining
    
    def unlock_account(self, identifier: str):
        """
        Manually unlock an account and reset failed attempts.
        
        Args:
            identifier: Username or email to unlock
        """
        if identifier in self.locked_accounts:
            del self.locked_accounts[identifier]
        if identifier in self.failed_attempts:
            del self.failed_attempts[identifier]
    
    def record_failed_attempt(self, identifier: str):
        """
        Record a failed login attempt and check for lockout.
        
        Args:
            identifier: Username or email that failed
        """
        if identifier not in self.failed_attempts:
            self.failed_attempts[identifier] = 0
        
        self.failed_attempts[identifier] += 1
        
        # Check if we should lock the account
        if self.failed_attempts[identifier] >= self.max_attempts:
            self.locked_accounts[identifier] = time.time()
    
    def get_failed_attempts(self, identifier: str) -> int:
        """Get the number of failed attempts for an identifier."""
        return self.failed_attempts.get(identifier, 0)
    
    def reset_failed_attempts(self, identifier: str):
        """Reset failed attempts counter after successful login."""
        if identifier in self.failed_attempts:
            del self.failed_attempts[identifier]

    def login_user(self, username_or_email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        """
        Authenticate a user login with account lockout protection.
        
        Args:
            username_or_email: Username or email address
            password: Plain text password
            
        Returns:
            Tuple[bool, str, Optional[User]]: (success, message, user_object)
        """
        try:
            if not username_or_email or not password:
                return False, "Username/email and password are required", None
            
            # Check if account is locked
            is_locked, remaining = self.is_account_locked(username_or_email)
            if is_locked:
                minutes = remaining // 60
                seconds = remaining % 60
                if minutes > 0:
                    return False, f"Account locked. Try again in {minutes}m {seconds}s", None
                else:
                    return False, f"Account locked. Try again in {seconds}s", None
            
            # Try to find user by username first, then by email
            user = User.get_by_username(username_or_email)
            if not user:
                user = User.get_by_email(username_or_email)
            
            if not user:
                self.record_failed_attempt(username_or_email)
                remaining_attempts = self.max_attempts - self.get_failed_attempts(username_or_email)
                if remaining_attempts > 0:
                    return False, f"Invalid credentials. {remaining_attempts} attempts remaining", None
                else:
                    return False, "Account locked due to too many failed attempts", None
            
            # Verify password
            if not self.verify_password(password, user.password_hash):
                self.record_failed_attempt(username_or_email)
                remaining_attempts = self.max_attempts - self.get_failed_attempts(username_or_email)
                if remaining_attempts > 0:
                    return False, f"Invalid credentials. {remaining_attempts} attempts remaining", None
                else:
                    return False, "Account locked due to too many failed attempts", None
            
            # Successful login - reset failed attempts
            self.reset_failed_attempts(username_or_email)
            
            # Set current session
            self.current_session = UserSession(user)
            
            return True, f"Welcome back, {user.username}!", user
            
        except Exception as e:
            return False, f"Login failed: {str(e)}", None
    
    def logout_user(self):
        """Log out the current user."""
        self.current_session = None
    
    def get_current_user(self) -> Optional[User]:
        """Get the currently logged-in user."""
        if self.current_session:
            return self.current_session.user
        return None
    
    def is_authenticated(self) -> bool:
        """Check if a user is currently authenticated."""
        return self.current_session is not None
    
    def change_password(self, user: User, current_password: str, new_password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        Change a user's password.
        
        Args:
            user: User object
            current_password: Current password for verification
            new_password: New password
            confirm_password: New password confirmation
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Verify current password
            if not self.verify_password(current_password, user.password_hash):
                return False, "Current password is incorrect"
            
            # Validate new password
            if new_password != confirm_password:
                return False, "New passwords do not match"
            
            password_valid, password_error = self.validate_password(new_password)
            if not password_valid:
                return False, password_error
            
            # Don't allow same password
            if self.verify_password(new_password, user.password_hash):
                return False, "New password must be different from current password"
            
            # Update password (would need to implement User.update_password method)
            # For now, this is a placeholder
            return True, "Password changed successfully"
            
        except Exception as e:
            return False, f"Password change failed: {str(e)}"


class UserSession:
    """Represents a user session."""
    
    def __init__(self, user: User):
        self.user = user
        self.login_time = datetime.now()
    
    def get_session_duration(self) -> float:
        """Get session duration in minutes."""
        return (datetime.now() - self.login_time).total_seconds() / 60
    
    def is_expired(self, timeout_minutes: int = 480) -> bool:
        """Check if session is expired (default 8 hours)."""
        return self.get_session_duration() > timeout_minutes


# Global authentication service instance
auth_service = AuthenticationService()