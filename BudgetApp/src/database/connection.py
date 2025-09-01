"""
Database connection and management module.
Handles SQLite database connection, initialization, and basic operations.
"""

import sqlite3
import os
from pathlib import Path
from typing import Optional, Union
from contextlib import contextmanager


class DatabaseConnection:
    """Manages SQLite database connection and operations."""
    
    def __init__(self, db_path: Union[str, Path] = None):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to the SQLite database file. If None, uses default location.
        """
        if db_path is None:
            # Create data directory in user's home folder
            data_dir = Path.home() / ".budgetapp"
            data_dir.mkdir(exist_ok=True)
            self.db_path = data_dir / "budget.db"
        else:
            self.db_path = Path(db_path)
        
        self._connection = None
    
    def connect(self) -> sqlite3.Connection:
        """
        Create and return a database connection.
        
        Returns:
            sqlite3.Connection: Database connection object
        """
        connection = sqlite3.connect(str(self.db_path))
        connection.row_factory = sqlite3.Row  # Enable dict-like access to rows
        connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign key constraints
        return connection
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        Automatically handles connection cleanup.
        
        Usage:
            with db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users")
        """
        conn = self.connect()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def execute_script(self, script: str) -> None:
        """
        Execute a SQL script (multiple statements).
        
        Args:
            script: SQL script content
        """
        with self.get_connection() as conn:
            conn.executescript(script)
    
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Execute a SELECT query and return results.
        
        Args:
            query: SQL SELECT statement
            params: Query parameters
            
        Returns:
            list: Query results as list of Row objects
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.fetchall()
    
    def execute_command(self, command: str, params: tuple = ()) -> int:
        """
        Execute an INSERT, UPDATE, or DELETE command.
        
        Args:
            command: SQL command
            params: Command parameters
            
        Returns:
            int: Number of affected rows or last row ID for INSERT
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(command, params)
            return cursor.lastrowid if command.strip().upper().startswith('INSERT') else cursor.rowcount
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table to check
            
        Returns:
            bool: True if table exists, False otherwise
        """
        query = """
        SELECT COUNT(*) 
        FROM sqlite_master 
        WHERE type='table' AND name=?
        """
        result = self.execute_query(query, (table_name,))
        return result[0][0] > 0
    
    def get_database_info(self) -> dict:
        """
        Get basic information about the database.
        
        Returns:
            dict: Database information including file size, table count, etc.
        """
        info = {
            'db_path': str(self.db_path),
            'exists': self.db_path.exists(),
            'size_bytes': self.db_path.stat().st_size if self.db_path.exists() else 0,
        }
        
        if info['exists']:
            tables = self.execute_query(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            info['tables'] = [row[0] for row in tables]
            info['table_count'] = len(info['tables'])
        else:
            info['tables'] = []
            info['table_count'] = 0
        
        return info


# Global database instance
db = DatabaseConnection()