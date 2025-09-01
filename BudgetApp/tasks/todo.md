# Budget App Development Plan

## Project Overview
Creating a Python-based monthly budgeting application with:
- Multi-user support with data security/separation
- GUI interface with navigation
- Data input for expenses, savings, and goals by category
- Overview dashboard with monthly summaries and comparisons
- Optional data sharing between users via secure tokens
- Database storage

## Technology Stack
- **GUI Framework**: Tkinter (built-in Python library)
- **Database**: SQLite (simple, file-based, no server required)
- **Authentication**: Custom implementation with bcrypt password hashing
- **Data Sharing**: UUID-based tokens with permission system
- **Testing**: pytest for unit tests

## Development Phases

### Phase 1: Foundation ✅
- [x] Create GitHub repository for budget app
- [ ] Clone repository locally and set up basic structure
- [ ] Create tasks/todo.md with comprehensive development plan
- [ ] Set up Python project files (requirements.txt, .gitignore)

### Phase 2: Database & Core Infrastructure
- [ ] Choose and configure database technology (SQLite)
- [ ] Design database schema for users, expenses, savings, and goals
- [ ] Implement database models and connection handling
- [ ] Create database initialization and migration scripts

### Phase 3: User Authentication & Security
- [ ] Implement user authentication and security system
- [ ] Add password hashing and validation
- [ ] Create user session management
- [ ] Implement data isolation between users

### Phase 4: GUI Framework
- [ ] Create main application window with Tkinter
- [ ] Design navigation system between sections
- [ ] Create reusable GUI components
- [ ] Implement responsive layout system

### Phase 5: Data Input Features
- [ ] Build expense input forms with category selection
- [ ] Create savings input interface
- [ ] Implement goals tracking input system
- [ ] Add data validation and error handling

### Phase 6: Overview Dashboard
- [ ] Create monthly expense summary by category
- [ ] Implement savings tracking by goal/category
- [ ] Add overage/underage calculations
- [ ] Build comparison views (previous/current/next month)

### Phase 7: Data Sharing & Advanced Features
- [ ] Implement data sharing mechanism with tokens/secure IDs
- [ ] Create permission system for shared data
- [ ] Add data export functionality
- [ ] Implement backup and restore features

### Phase 8: Testing & Documentation
- [ ] Add unit tests for core functionality
- [ ] Create integration tests for GUI components
- [ ] Write user documentation and README
- [ ] Add code documentation and comments

## Database Schema Design
```sql
-- Users table for authentication
users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories for organizing expenses/savings/goals
categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('expense', 'savings', 'goal')),
    user_id INTEGER REFERENCES users(id),
    color TEXT DEFAULT '#000000'
);

-- Expense tracking
expenses (
    id INTEGER PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    date DATE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Savings tracking
savings (
    id INTEGER PRIMARY KEY,
    amount DECIMAL(10,2) NOT NULL,
    description TEXT,
    category_id INTEGER REFERENCES categories(id),
    date DATE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Goals with targets and progress
goals (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    target_amount DECIMAL(10,2) NOT NULL,
    current_amount DECIMAL(10,2) DEFAULT 0,
    deadline DATE,
    category_id INTEGER REFERENCES categories(id),
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Data sharing between users
shared_data (
    id INTEGER PRIMARY KEY,
    owner_user_id INTEGER REFERENCES users(id),
    shared_user_id INTEGER REFERENCES users(id),
    data_type TEXT NOT NULL CHECK (data_type IN ('expense', 'savings', 'goal', 'category')),
    data_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    permissions TEXT DEFAULT 'read',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## File Structure
```
BudgetApp/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py        # Database models
│   │   └── connection.py    # Database connection handling
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py   # Main application window
│   │   ├── navigation.py    # Navigation system
│   │   └── components/      # Reusable GUI components
│   ├── auth/
│   │   ├── __init__.py
│   │   └── authentication.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
├── tasks/
│   └── todo.md
├── requirements.txt
├── .gitignore
└── README.md
```

## Development Principles
1. **Simplicity First**: Keep each change small and focused
2. **Modular Design**: Each component should be independent
3. **Progressive Enhancement**: Start with basic features, add complexity gradually
4. **Security by Design**: Implement proper data isolation from the start
5. **User Experience**: Intuitive navigation and clear feedback

## Review Section
*To be completed as development progresses*

---
Repository: https://github.com/marcus-gray/BudgetApp