# Budget App

A modern, secure Python-based monthly budgeting application with enterprise-grade authentication and sleek CustomTkinter interface.

![Budget App](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![GUI](https://img.shields.io/badge/GUI-CustomTkinter-purple.svg)
![Database](https://img.shields.io/badge/Database-SQLite-orange.svg)

## ✨ Features

### 🔐 Enterprise-Grade Security
- **Secure Authentication**: bcrypt password hashing with comprehensive validation
- **Account Lockout Protection**: 5-attempt limit with 15-minute automatic reset
- **Password Reset System**: Token-based reset with 3-step verification process
- **Emergency Bypass**: Administrative lockout override for account recovery
- **Session Management**: Proper authentication state with timeout support

### 💻 Modern User Interface
- **CustomTkinter GUI**: Sleek, professional appearance that doesn't look like legacy software
- **Dark/Light Themes**: Automatic theme switching with consistent styling
- **Responsive Design**: Adapts to window resizing with proper grid management
- **Intuitive Navigation**: Sidebar navigation with smooth hover effects
- **Color-Coded Feedback**: Red/green for expenses/income, status-based messages

### 💰 Financial Management
- **Expense Tracking**: Add, categorize, and manage expenses with validation
- **Dynamic Categories**: Create and manage custom expense categories
- **Monthly Overview**: Financial dashboard with key metrics and summaries
- **Goals Progress**: Visual progress bars and completion tracking
- **Transaction History**: Combined view of all financial activities

### 🗄️ Robust Data Management
- **SQLite Database**: File-based storage with zero configuration
- **Data Isolation**: Complete separation of user data for security
- **ACID Compliance**: Reliable transactions with rollback capability
- **Automatic Cleanup**: Expired tokens and sessions cleaned automatically
- **Foreign Key Integrity**: Proper relationships prevent data corruption

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/marcus-gray/BudgetApp.git
cd BudgetApp
```

2. **Create a virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
python src/main.py
```

The application will:
- Initialize the SQLite database automatically
- Create the main window with login screen
- Set up default categories for new users

## 📱 Usage

### First Time Setup
1. **Create Account**: Click "Sign Up" and fill in your details
2. **Secure Password**: Use a strong password meeting the requirements
3. **Login**: Use your credentials to access the dashboard

### Managing Finances
1. **Add Expenses**: Navigate to Expenses → Fill out the form → Submit
2. **View Dashboard**: Overview page shows monthly summaries and trends
3. **Track Goals**: Monitor progress toward financial objectives
4. **Browse History**: Review past transactions by month

### Account Recovery
1. **Forgot Password**: Click "Forgot your password?" on login screen
2. **Generate Token**: Enter username/email to get reset token
3. **Reset Password**: Verify token and set new password
4. **Emergency Unlock**: Use bypass system if account is locked

## 🏗️ Architecture

### Project Structure
```
BudgetApp/
├── src/
│   ├── main.py              # Application entry point
│   ├── database/            # Database models and connections
│   ├── auth/               # Authentication and security
│   ├── gui/                # User interface components
│   └── utils/              # Helper functions
├── tests/                  # Test files
├── tasks/                  # Development tracking
└── requirements.txt        # Dependencies
```

### Technology Stack
- **Python 3.8+**: Modern Python with type hints
- **CustomTkinter 5.2.2**: Modern GUI framework
- **SQLite**: Embedded database with ACID compliance
- **bcrypt**: Secure password hashing
- **pytest**: Testing framework (ready for test development)

### Security Features
- **Password Validation**: 8+ characters with complexity requirements
- **Token Security**: Cryptographically secure tokens with expiration
- **Failed Attempt Tracking**: Progressive lockout with attempt counting
- **Session Management**: Proper authentication state handling
- **Emergency Recovery**: Administrative bypass for account access

## 🔧 Development

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (when available)
pytest

# Run the application in development mode
python src/main.py
```

### Database Management
The application uses SQLite with automatic initialization:
- Database file: `~/.budgetapp/budget.db`
- Schema: Defined in `src/database/init_db.py`
- Models: Located in `src/database/models.py`

## 📊 Features in Detail

### Authentication System
- **Registration**: Username, email, and password validation
- **Login**: Support for username or email authentication
- **Password Reset**: 3-step token-based reset process
- **Account Lockout**: Protection against brute force attempts
- **Emergency Bypass**: Administrative unlock capabilities

### Financial Tracking
- **Expense Categories**: Housing, Food, Transportation, etc.
- **Date Handling**: Flexible date input with quick-select options
- **Amount Validation**: Decimal precision with proper formatting
- **Transaction Lists**: Sortable, filterable transaction history

### User Interface
- **Theme Support**: Dark and light modes with smooth transitions
- **Responsive Layout**: Grid-based layout that adapts to window size
- **Status Feedback**: Color-coded messages for user actions
- **Modern Components**: Cards, buttons, and forms with contemporary styling

## 🔮 Future Enhancements

### Planned Features
- **Savings Management**: Dedicated savings tracking with goals
- **Advanced Goals**: CRUD operations for financial objectives
- **Reports & Analytics**: Charts and detailed financial analysis
- **Data Export**: CSV/PDF export for backup and analysis
- **Data Sharing**: Secure sharing between users with tokens
- **Recurring Transactions**: Automated recurring expenses and savings

### Technical Improvements
- **Test Coverage**: Comprehensive unit and integration tests
- **Performance Optimization**: Database query optimization
- **Advanced Themes**: More color schemes and customization
- **Plugin System**: Extensible architecture for custom features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

### Getting Help
- **Issues**: Report bugs and request features on GitHub
- **Documentation**: Check the `tasks/todo.md` for detailed development notes
- **Security**: For security issues, please email directly (not public issues)

### System Requirements
- **Python**: 3.8 or higher
- **OS**: Windows, macOS, or Linux
- **Memory**: 100MB RAM minimum
- **Storage**: 50MB available space

## 🏆 Achievements

✅ **Professional Grade Security**: Enterprise-level authentication  
✅ **Modern User Interface**: Sleek design rivaling commercial apps  
✅ **Comprehensive Data Management**: Full CRUD with proper validation  
✅ **Robust Architecture**: Modular design following best practices  
✅ **Excellent User Experience**: Intuitive navigation with helpful feedback  

---

**Repository**: [https://github.com/marcus-gray/BudgetApp](https://github.com/marcus-gray/BudgetApp)

Built with ❤️ using Python and CustomTkinter