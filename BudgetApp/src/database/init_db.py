"""
Database initialization script.
Creates all necessary tables and sets up the database schema.
"""

from .connection import db


def create_tables():
    """Create all database tables with proper schema."""
    
    schema_sql = """
    -- Users table for authentication
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Categories for organizing expenses/savings/goals
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL CHECK (type IN ('expense', 'savings', 'goal')),
        user_id INTEGER NOT NULL,
        color TEXT DEFAULT '#000000',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    -- Expense tracking
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount DECIMAL(10,2) NOT NULL,
        description TEXT,
        category_id INTEGER NOT NULL,
        date DATE NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    -- Savings tracking
    CREATE TABLE IF NOT EXISTS savings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount DECIMAL(10,2) NOT NULL,
        description TEXT,
        category_id INTEGER NOT NULL,
        date DATE NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    -- Goals with targets and progress
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        target_amount DECIMAL(10,2) NOT NULL,
        current_amount DECIMAL(10,2) DEFAULT 0,
        deadline DATE,
        category_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    -- Data sharing between users
    CREATE TABLE IF NOT EXISTS shared_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner_user_id INTEGER NOT NULL,
        shared_user_id INTEGER NOT NULL,
        data_type TEXT NOT NULL CHECK (data_type IN ('expense', 'savings', 'goal', 'category')),
        data_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        permissions TEXT DEFAULT 'read',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (shared_user_id) REFERENCES users (id) ON DELETE CASCADE
    );

    -- Indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_categories_user_id ON categories (user_id);
    CREATE INDEX IF NOT EXISTS idx_categories_type ON categories (type);
    CREATE INDEX IF NOT EXISTS idx_expenses_user_id ON expenses (user_id);
    CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses (date);
    CREATE INDEX IF NOT EXISTS idx_expenses_category_id ON expenses (category_id);
    CREATE INDEX IF NOT EXISTS idx_savings_user_id ON savings (user_id);
    CREATE INDEX IF NOT EXISTS idx_savings_date ON savings (date);
    CREATE INDEX IF NOT EXISTS idx_savings_category_id ON savings (category_id);
    CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals (user_id);
    CREATE INDEX IF NOT EXISTS idx_shared_data_token ON shared_data (token);
    CREATE INDEX IF NOT EXISTS idx_shared_data_owner ON shared_data (owner_user_id);
    """
    
    db.execute_script(schema_sql)


def create_default_categories(user_id: int):
    """Create default categories for a new user."""
    
    default_categories = [
        # Expense categories
        ('Housing', 'expense', '#FF6B6B'),
        ('Food & Dining', 'expense', '#4ECDC4'),
        ('Transportation', 'expense', '#45B7D1'),
        ('Utilities', 'expense', '#96CEB4'),
        ('Healthcare', 'expense', '#FFEAA7'),
        ('Entertainment', 'expense', '#DDA0DD'),
        ('Shopping', 'expense', '#98D8C8'),
        ('Personal Care', 'expense', '#F7DC6F'),
        ('Other', 'expense', '#AED6F1'),
        
        # Savings categories
        ('Emergency Fund', 'savings', '#27AE60'),
        ('Vacation', 'savings', '#3498DB'),
        ('Retirement', 'savings', '#9B59B6'),
        ('Investment', 'savings', '#E67E22'),
        ('Education', 'savings', '#F39C12'),
        
        # Goal categories
        ('House Down Payment', 'goal', '#2ECC71'),
        ('Car Purchase', 'goal', '#3498DB'),
        ('Debt Payoff', 'goal', '#E74C3C'),
        ('Major Purchase', 'goal', '#F39C12'),
    ]
    
    for name, type, color in default_categories:
        query = """
        INSERT OR IGNORE INTO categories (name, type, user_id, color)
        VALUES (?, ?, ?, ?)
        """
        db.execute_command(query, (name, type, user_id, color))


def initialize_database():
    """Initialize the database with all tables and setup."""
    print("Initializing database...")
    
    # Create all tables
    create_tables()
    
    # Check database info
    info = db.get_database_info()
    print(f"Database created at: {info['db_path']}")
    print(f"Tables created: {', '.join(info['tables'])}")
    print("Database initialization complete!")
    
    return info


def reset_database():
    """Reset the database by dropping all tables and recreating them."""
    drop_tables_sql = """
    DROP TABLE IF EXISTS shared_data;
    DROP TABLE IF EXISTS goals;
    DROP TABLE IF EXISTS savings;
    DROP TABLE IF EXISTS expenses;
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS users;
    """
    
    db.execute_script(drop_tables_sql)
    create_tables()
    print("Database reset complete!")


if __name__ == "__main__":
    # Run database initialization
    initialize_database()