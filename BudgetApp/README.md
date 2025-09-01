# Budget App

A Python-based monthly budgeting application with multi-user support and GUI interface.

## Features

- **Multi-user Support**: Secure user authentication with data isolation
- **Expense Tracking**: Categorized expense input and tracking
- **Savings Management**: Track savings by goals and categories
- **Monthly Overview**: Comprehensive dashboard with comparisons
- **Data Sharing**: Optional secure data sharing between users
- **User-friendly GUI**: Intuitive Tkinter-based interface

## Technology Stack

- **Python 3.8+**
- **Tkinter** for GUI
- **SQLite** for database
- **bcrypt** for password hashing
- **pytest** for testing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/marcus-gray/BudgetApp.git
cd BudgetApp
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python src/main.py
```

## Development

See `tasks/todo.md` for the complete development roadmap and current progress.

## License

MIT License