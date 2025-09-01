"""
Budget App - Main application entry point.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

# Initialize database
from database.init_db import initialize_database

def main():
    """Main application entry point."""
    try:
        # Initialize database
        print("Starting Budget App...")
        initialize_database()
        
        # Import and start GUI
        from gui.main_window import MainWindow
        
        # Create and run the application
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()