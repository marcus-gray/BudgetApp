"""
Expenses page with modern forms for tracking and managing expenses.
"""

import customtkinter as ctk
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from ..components.theme_manager import theme_manager
from ...database.models import User, Category, Expense


class ExpensesFrame(ctk.CTkFrame):
    """Modern expenses tracking interface."""
    
    def __init__(self, parent, user: User):
        super().__init__(parent)
        self.user = user
        self.expenses = []
        self.categories = []
        
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Load data
        self.load_data()
        
        # Create interface
        self.create_interface()
    
    def load_data(self):
        """Load expenses and categories from database."""
        if self.user and self.user.id:
            self.categories = Category.get_by_user(self.user.id, 'expense')
            self.expenses = Expense.get_by_user(self.user.id)
    
    def create_interface(self):
        """Create the main interface layout."""
        # Left panel - Add expense form
        self.create_expense_form()
        
        # Right panel - Expenses list
        self.create_expenses_list()
    
    def create_expense_form(self):
        """Create the expense input form."""
        form_frame = ctk.CTkFrame(self, width=350)
        form_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=0)
        form_frame.grid_propagate(False)
        
        # Header
        header_label = ctk.CTkLabel(
            form_frame,
            text="💸 Add Expense",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header_label.pack(pady=(20, 30))
        
        # Form container
        form_container = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Amount field
        self.amount_var = ctk.StringVar()
        self.create_form_field(form_container, "Amount ($)", self.amount_var, 0)
        self.amount_entry = form_container.winfo_children()[-1]
        
        # Description field
        self.description_var = ctk.StringVar()
        self.create_form_field(form_container, "Description", self.description_var, 1)
        
        # Category dropdown
        self.create_category_field(form_container, 2)
        
        # Date field
        self.create_date_field(form_container, 3)
        
        # Add button
        add_button = ctk.CTkButton(
            form_container,
            text="Add Expense",
            command=self.add_expense,
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            **theme_manager.get_button_style("primary")
        )
        add_button.pack(fill="x", pady=(20, 10))
        
        # Clear button
        clear_button = ctk.CTkButton(
            form_container,
            text="Clear Form",
            command=self.clear_form,
            font=ctk.CTkFont(size=12),
            height=35,
            **theme_manager.get_button_style("secondary")
        )
        clear_button.pack(fill="x", pady=(5, 10))
        
        # Status label
        self.status_label = ctk.CTkLabel(
            form_container,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=300
        )
        self.status_label.pack(pady=10)
    
    def create_form_field(self, parent, label_text: str, variable: ctk.StringVar, row: int):
        """Create a form field with label and entry."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text=label_text,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", pady=(10, 5))
        
        # Entry
        entry = ctk.CTkEntry(
            parent,
            textvariable=variable,
            font=ctk.CTkFont(size=14),
            height=35,
            **theme_manager.get_input_style()
        )
        entry.pack(fill="x", pady=(0, 10))
        
        return entry
    
    def create_category_field(self, parent, row: int):
        """Create category selection dropdown."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text="Category",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", pady=(10, 5))
        
        # Dropdown
        category_names = [cat.name for cat in self.categories] if self.categories else ["No categories available"]
        self.category_var = ctk.StringVar(value=category_names[0] if category_names else "")
        
        self.category_dropdown = ctk.CTkOptionMenu(
            parent,
            variable=self.category_var,
            values=category_names,
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.category_dropdown.pack(fill="x", pady=(0, 10))
        
        # Add category button
        add_cat_button = ctk.CTkButton(
            parent,
            text="+ Add Category",
            command=self.show_add_category_dialog,
            font=ctk.CTkFont(size=11),
            height=25,
            **theme_manager.get_button_style("secondary")
        )
        add_cat_button.pack(fill="x", pady=(0, 10))
    
    def create_date_field(self, parent, row: int):
        """Create date selection field."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text="Date",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x", pady=(10, 5))
        
        # Date container
        date_frame = ctk.CTkFrame(parent, fg_color="transparent")
        date_frame.pack(fill="x", pady=(0, 10))
        
        # Date entry
        self.date_var = ctk.StringVar(value=date.today().strftime("%Y-%m-%d"))
        date_entry = ctk.CTkEntry(
            date_frame,
            textvariable=self.date_var,
            font=ctk.CTkFont(size=14),
            height=35,
            **theme_manager.get_input_style()
        )
        date_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # Today button
        today_button = ctk.CTkButton(
            date_frame,
            text="Today",
            command=lambda: self.date_var.set(date.today().strftime("%Y-%m-%d")),
            font=ctk.CTkFont(size=11),
            width=60,
            height=35,
            **theme_manager.get_button_style("secondary")
        )
        today_button.pack(side="right")
    
    def create_expenses_list(self):
        """Create the expenses list display."""
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.grid_columnconfigure(1, weight=1)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Recent Expenses",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Total display
        self.total_label = ctk.CTkLabel(
            header_frame,
            text="Total: $0.00",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=theme_manager.get_color("danger")
        )
        self.total_label.grid(row=0, column=1, sticky="e")
        
        # Scrollable list
        self.expenses_scrollable = ctk.CTkScrollableFrame(list_frame)
        self.expenses_scrollable.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Refresh expenses list
        self.refresh_expenses_list()
    
    def refresh_expenses_list(self):
        """Refresh the expenses list display."""
        # Clear existing items
        for widget in self.expenses_scrollable.winfo_children():
            widget.destroy()
        
        # Reload data
        self.load_data()
        
        if not self.expenses:
            # Empty state
            empty_label = ctk.CTkLabel(
                self.expenses_scrollable,
                text="No expenses recorded yet.\nAdd your first expense using the form on the left!",
                font=ctk.CTkFont(size=14),
                text_color=theme_manager.get_color("text_secondary")
            )
            empty_label.pack(pady=50)
            self.total_label.configure(text="Total: $0.00")
            return
        
        # Calculate total
        total = sum(expense.amount for expense in self.expenses)
        self.total_label.configure(text=f"Total: ${total:.2f}")
        
        # Create expense items
        for expense in self.expenses:
            self.create_expense_item(expense)
    
    def create_expense_item(self, expense: Expense):
        """Create an individual expense item."""
        item_frame = ctk.CTkFrame(self.expenses_scrollable, **theme_manager.get_card_style())
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Main content frame
        content_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Amount (left)
        amount_label = ctk.CTkLabel(
            content_frame,
            text=f"${expense.amount:.2f}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=theme_manager.get_color("danger")
        )
        amount_label.grid(row=0, column=0, sticky="w", padx=(0, 15))
        
        # Description and details (center)
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.grid(row=0, column=1, sticky="ew")
        
        desc_label = ctk.CTkLabel(
            details_frame,
            text=expense.description or "No description",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        desc_label.pack(anchor="w")
        
        # Category and date
        category_name = "Unknown"
        if expense.category_id:
            category = next((cat for cat in self.categories if cat.id == expense.category_id), None)
            if category:
                category_name = category.name
        
        info_label = ctk.CTkLabel(
            details_frame,
            text=f"{category_name} • {expense.date.strftime('%B %d, %Y')}",
            font=ctk.CTkFont(size=12),
            text_color=theme_manager.get_color("text_secondary"),
            anchor="w"
        )
        info_label.pack(anchor="w", pady=(2, 0))
        
        # Actions (right)
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.grid(row=0, column=2, sticky="e")
        
        edit_button = ctk.CTkButton(
            actions_frame,
            text="Edit",
            command=lambda: self.edit_expense(expense),
            font=ctk.CTkFont(size=11),
            width=50,
            height=25,
            **theme_manager.get_button_style("secondary")
        )
        edit_button.pack(side="right", padx=(5, 0))
        
        delete_button = ctk.CTkButton(
            actions_frame,
            text="Delete",
            command=lambda: self.delete_expense(expense),
            font=ctk.CTkFont(size=11),
            width=50,
            height=25,
            **theme_manager.get_button_style("danger")
        )
        delete_button.pack(side="right")
    
    def add_expense(self):
        """Add a new expense."""
        try:
            # Validate inputs
            amount_str = self.amount_var.get().strip()
            if not amount_str:
                self.show_status("Please enter an amount", "error")
                return
            
            # Parse amount
            try:
                amount = Decimal(amount_str)
                if amount <= 0:
                    self.show_status("Amount must be greater than 0", "error")
                    return
            except (ValueError, TypeError):
                self.show_status("Please enter a valid amount", "error")
                return
            
            # Get description
            description = self.description_var.get().strip()
            if not description:
                self.show_status("Please enter a description", "error")
                return
            
            # Get category
            category_name = self.category_var.get()
            if not category_name or category_name == "No categories available":
                self.show_status("Please select a category", "error")
                return
            
            category = next((cat for cat in self.categories if cat.name == category_name), None)
            if not category:
                self.show_status("Invalid category selected", "error")
                return
            
            # Parse date
            try:
                expense_date = datetime.strptime(self.date_var.get(), "%Y-%m-%d").date()
            except ValueError:
                self.show_status("Please enter a valid date (YYYY-MM-DD)", "error")
                return
            
            # Create expense
            expense = Expense.create(
                amount=amount,
                description=description,
                category_id=category.id,
                user_id=self.user.id,
                date=expense_date
            )
            
            if expense:
                self.show_status(f"Expense added: ${amount}", "success")
                self.clear_form()
                self.refresh_expenses_list()
            else:
                self.show_status("Failed to add expense", "error")
                
        except Exception as e:
            self.show_status(f"Error adding expense: {str(e)}", "error")
    
    def clear_form(self):
        """Clear the expense form."""
        self.amount_var.set("")
        self.description_var.set("")
        self.date_var.set(date.today().strftime("%Y-%m-%d"))
        if self.categories:
            self.category_var.set(self.categories[0].name)
        self.clear_status()
    
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
    
    def show_add_category_dialog(self):
        """Show dialog to add a new category."""
        # Simple input dialog (could be enhanced with custom dialog)
        dialog = ctk.CTkInputDialog(
            text="Enter category name:",
            title="Add Category"
        )
        name = dialog.get_input()
        
        if name and name.strip():
            try:
                category = Category.create(
                    name=name.strip(),
                    type='expense',
                    user_id=self.user.id,
                    color="#FF6B6B"  # Default color
                )
                
                if category:
                    self.load_data()  # Reload categories
                    
                    # Update dropdown
                    category_names = [cat.name for cat in self.categories]
                    self.category_dropdown.configure(values=category_names)
                    self.category_var.set(name.strip())
                    
                    self.show_status(f"Category '{name.strip()}' added", "success")
                else:
                    self.show_status("Failed to add category", "error")
                    
            except Exception as e:
                self.show_status(f"Error adding category: {str(e)}", "error")
    
    def edit_expense(self, expense: Expense):
        """Edit an existing expense (placeholder)."""
        self.show_status("Edit functionality coming soon!", "info")
    
    def delete_expense(self, expense: Expense):
        """Delete an expense (placeholder)."""
        self.show_status("Delete functionality coming soon!", "info")