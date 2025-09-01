"""
Database models and data access layer.
Contains classes for interacting with database tables and business logic.
"""

from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any
from .connection import db


@dataclass
class User:
    """User model for authentication and data ownership."""
    id: Optional[int] = None
    username: str = ""
    email: str = ""
    password_hash: str = ""
    created_at: Optional[datetime] = None
    
    @classmethod
    def create(cls, username: str, email: str, password_hash: str) -> 'User':
        """Create a new user in the database."""
        query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (?, ?, ?)
        """
        user_id = db.execute_command(query, (username, email, password_hash))
        return cls.get_by_id(user_id)
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional['User']:
        """Get user by ID."""
        query = "SELECT * FROM users WHERE id = ?"
        results = db.execute_query(query, (user_id,))
        return cls._from_row(results[0]) if results else None
    
    @classmethod
    def get_by_username(cls, username: str) -> Optional['User']:
        """Get user by username."""
        query = "SELECT * FROM users WHERE username = ?"
        results = db.execute_query(query, (username,))
        return cls._from_row(results[0]) if results else None
    
    @classmethod
    def get_by_email(cls, email: str) -> Optional['User']:
        """Get user by email."""
        query = "SELECT * FROM users WHERE email = ?"
        results = db.execute_query(query, (email,))
        return cls._from_row(results[0]) if results else None
    
    @classmethod
    def _from_row(cls, row) -> 'User':
        """Create User instance from database row."""
        return cls(
            id=row['id'],
            username=row['username'],
            email=row['email'],
            password_hash=row['password_hash'],
            created_at=datetime.fromisoformat(row['created_at'])
        )


@dataclass
class Category:
    """Category model for organizing expenses, savings, and goals."""
    id: Optional[int] = None
    name: str = ""
    type: str = ""  # 'expense', 'savings', 'goal'
    user_id: int = 0
    color: str = "#000000"
    
    @classmethod
    def create(cls, name: str, type: str, user_id: int, color: str = "#000000") -> 'Category':
        """Create a new category."""
        query = """
        INSERT INTO categories (name, type, user_id, color)
        VALUES (?, ?, ?, ?)
        """
        category_id = db.execute_command(query, (name, type, user_id, color))
        return cls.get_by_id(category_id)
    
    @classmethod
    def get_by_id(cls, category_id: int) -> Optional['Category']:
        """Get category by ID."""
        query = "SELECT * FROM categories WHERE id = ?"
        results = db.execute_query(query, (category_id,))
        return cls._from_row(results[0]) if results else None
    
    @classmethod
    def get_by_user(cls, user_id: int, type: str = None) -> List['Category']:
        """Get all categories for a user, optionally filtered by type."""
        if type:
            query = "SELECT * FROM categories WHERE user_id = ? AND type = ? ORDER BY name"
            results = db.execute_query(query, (user_id, type))
        else:
            query = "SELECT * FROM categories WHERE user_id = ? ORDER BY name"
            results = db.execute_query(query, (user_id,))
        
        return [cls._from_row(row) for row in results]
    
    @classmethod
    def _from_row(cls, row) -> 'Category':
        """Create Category instance from database row."""
        return cls(
            id=row['id'],
            name=row['name'],
            type=row['type'],
            user_id=row['user_id'],
            color=row['color']
        )


@dataclass
class Expense:
    """Expense tracking model."""
    id: Optional[int] = None
    amount: Decimal = Decimal('0.00')
    description: str = ""
    category_id: int = 0
    date: date = None
    user_id: int = 0
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.date is None:
            self.date = date.today()
    
    @classmethod
    def create(cls, amount: Decimal, description: str, category_id: int, 
               user_id: int, date: date = None) -> 'Expense':
        """Create a new expense."""
        if date is None:
            date = date.today()
        
        query = """
        INSERT INTO expenses (amount, description, category_id, date, user_id)
        VALUES (?, ?, ?, ?, ?)
        """
        expense_id = db.execute_command(query, (float(amount), description, category_id, date, user_id))
        return cls.get_by_id(expense_id)
    
    @classmethod
    def get_by_id(cls, expense_id: int) -> Optional['Expense']:
        """Get expense by ID."""
        query = "SELECT * FROM expenses WHERE id = ?"
        results = db.execute_query(query, (expense_id,))
        return cls._from_row(results[0]) if results else None
    
    @classmethod
    def get_by_user(cls, user_id: int, start_date: date = None, end_date: date = None) -> List['Expense']:
        """Get expenses for a user, optionally filtered by date range."""
        if start_date and end_date:
            query = """
            SELECT * FROM expenses 
            WHERE user_id = ? AND date BETWEEN ? AND ? 
            ORDER BY date DESC
            """
            results = db.execute_query(query, (user_id, start_date, end_date))
        else:
            query = "SELECT * FROM expenses WHERE user_id = ? ORDER BY date DESC"
            results = db.execute_query(query, (user_id,))
        
        return [cls._from_row(row) for row in results]
    
    @classmethod
    def _from_row(cls, row) -> 'Expense':
        """Create Expense instance from database row."""
        return cls(
            id=row['id'],
            amount=Decimal(str(row['amount'])),
            description=row['description'],
            category_id=row['category_id'],
            date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
            user_id=row['user_id'],
            created_at=datetime.fromisoformat(row['created_at'])
        )


@dataclass
class Savings:
    """Savings tracking model."""
    id: Optional[int] = None
    amount: Decimal = Decimal('0.00')
    description: str = ""
    category_id: int = 0
    date: date = None
    user_id: int = 0
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.date is None:
            self.date = date.today()
    
    @classmethod
    def create(cls, amount: Decimal, description: str, category_id: int, 
               user_id: int, date: date = None) -> 'Savings':
        """Create a new savings entry."""
        if date is None:
            date = date.today()
        
        query = """
        INSERT INTO savings (amount, description, category_id, date, user_id)
        VALUES (?, ?, ?, ?, ?)
        """
        savings_id = db.execute_command(query, (float(amount), description, category_id, date, user_id))
        return cls.get_by_id(savings_id)
    
    @classmethod
    def get_by_id(cls, savings_id: int) -> Optional['Savings']:
        """Get savings by ID."""
        query = "SELECT * FROM savings WHERE id = ?"
        results = db.execute_query(query, (savings_id,))
        return cls._from_row(results[0]) if results else None
    
    @classmethod
    def get_by_user(cls, user_id: int, start_date: date = None, end_date: date = None) -> List['Savings']:
        """Get savings for a user, optionally filtered by date range."""
        if start_date and end_date:
            query = """
            SELECT * FROM savings 
            WHERE user_id = ? AND date BETWEEN ? AND ? 
            ORDER BY date DESC
            """
            results = db.execute_query(query, (user_id, start_date, end_date))
        else:
            query = "SELECT * FROM savings WHERE user_id = ? ORDER BY date DESC"
            results = db.execute_query(query, (user_id,))
        
        return [cls._from_row(row) for row in results]
    
    @classmethod
    def _from_row(cls, row) -> 'Savings':
        """Create Savings instance from database row."""
        return cls(
            id=row['id'],
            amount=Decimal(str(row['amount'])),
            description=row['description'],
            category_id=row['category_id'],
            date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
            user_id=row['user_id'],
            created_at=datetime.fromisoformat(row['created_at'])
        )


@dataclass
class Goal:
    """Goal tracking model with targets and progress."""
    id: Optional[int] = None
    name: str = ""
    target_amount: Decimal = Decimal('0.00')
    current_amount: Decimal = Decimal('0.00')
    deadline: Optional[date] = None
    category_id: int = 0
    user_id: int = 0
    created_at: Optional[datetime] = None
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage."""
        if self.target_amount == 0:
            return 0.0
        return float((self.current_amount / self.target_amount) * 100)
    
    @property
    def is_completed(self) -> bool:
        """Check if goal is completed."""
        return self.current_amount >= self.target_amount
    
    @classmethod
    def create(cls, name: str, target_amount: Decimal, category_id: int, 
               user_id: int, deadline: date = None) -> 'Goal':
        """Create a new goal."""
        query = """
        INSERT INTO goals (name, target_amount, category_id, user_id, deadline)
        VALUES (?, ?, ?, ?, ?)
        """
        goal_id = db.execute_command(query, (name, float(target_amount), category_id, user_id, deadline))
        return cls.get_by_id(goal_id)
    
    @classmethod
    def get_by_id(cls, goal_id: int) -> Optional['Goal']:
        """Get goal by ID."""
        query = "SELECT * FROM goals WHERE id = ?"
        results = db.execute_query(query, (goal_id,))
        return cls._from_row(results[0]) if results else None
    
    @classmethod
    def get_by_user(cls, user_id: int) -> List['Goal']:
        """Get all goals for a user."""
        query = "SELECT * FROM goals WHERE user_id = ? ORDER BY created_at DESC"
        results = db.execute_query(query, (user_id,))
        return [cls._from_row(row) for row in results]
    
    def update_progress(self, amount: Decimal) -> None:
        """Update goal progress."""
        self.current_amount = amount
        query = "UPDATE goals SET current_amount = ? WHERE id = ?"
        db.execute_command(query, (float(amount), self.id))
    
    @classmethod
    def _from_row(cls, row) -> 'Goal':
        """Create Goal instance from database row."""
        deadline = None
        if row['deadline']:
            deadline = datetime.strptime(row['deadline'], '%Y-%m-%d').date()
        
        return cls(
            id=row['id'],
            name=row['name'],
            target_amount=Decimal(str(row['target_amount'])),
            current_amount=Decimal(str(row['current_amount'])),
            deadline=deadline,
            category_id=row['category_id'],
            user_id=row['user_id'],
            created_at=datetime.fromisoformat(row['created_at'])
        )