"""
Overview dashboard showing financial summary and key metrics.
"""

import customtkinter as ctk
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from ..components.theme_manager import theme_manager
from ...database.models import User, Category, Expense, Savings, Goal


class OverviewFrame(ctk.CTkFrame):
    """Modern overview dashboard with financial summaries."""
    
    def __init__(self, parent, user: User):
        super().__init__(parent)
        self.user = user
        self.current_month = date.today().replace(day=1)
        
        # Configure grid
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Load data
        self.load_data()
        
        # Create interface
        self.create_interface()
    
    def load_data(self):
        """Load financial data for the current month."""
        if not self.user or not self.user.id:
            self.expenses = []
            self.savings = []
            self.goals = []
            return
        
        # Calculate date ranges
        start_date = self.current_month
        next_month = (start_date + timedelta(days=32)).replace(day=1)
        end_date = next_month - timedelta(days=1)
        
        # Load current month data
        self.expenses = Expense.get_by_user(self.user.id, start_date, end_date)
        self.savings = Savings.get_by_user(self.user.id, start_date, end_date)
        self.goals = Goal.get_by_user(self.user.id)
        
        # Load categories
        self.categories = Category.get_by_user(self.user.id)
    
    def create_interface(self):
        """Create the overview interface."""
        # Header
        self.create_header()
        
        # Summary cards
        self.create_summary_cards()
        
        # Recent activity and charts
        self.create_activity_section()
    
    def create_header(self):
        """Create the header section."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(
            header_frame,
            text="📊 Financial Overview",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # Month navigation
        month_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        month_frame.grid(row=0, column=1, sticky="e")
        
        # Previous month button
        prev_button = ctk.CTkButton(
            month_frame,
            text="◀",
            width=30,
            command=self.previous_month,
            **theme_manager.get_button_style("secondary")
        )
        prev_button.pack(side="left", padx=(0, 5))
        
        # Current month label
        self.month_label = ctk.CTkLabel(
            month_frame,
            text=self.current_month.strftime("%B %Y"),
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.month_label.pack(side="left", padx=10)
        
        # Next month button
        next_button = ctk.CTkButton(
            month_frame,
            text="▶",
            width=30,
            command=self.next_month,
            **theme_manager.get_button_style("secondary")
        )
        next_button.pack(side="left", padx=(5, 0))
    
    def create_summary_cards(self):
        """Create the summary cards section."""
        cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        cards_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=10)
        cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Calculate totals
        total_expenses = sum(exp.amount for exp in self.expenses)
        total_savings = sum(sav.amount for sav in self.savings)
        net_income = total_savings + total_expenses  # Simplified calculation
        
        # Expenses card
        self.create_summary_card(
            cards_frame, 
            "💸 Total Expenses", 
            f"${total_expenses:.2f}",
            theme_manager.get_color("danger"),
            0
        )
        
        # Savings card
        self.create_summary_card(
            cards_frame,
            "💰 Total Savings",
            f"${total_savings:.2f}",
            theme_manager.get_color("success"),
            1
        )
        
        # Net worth change (placeholder)
        net_change = total_savings - total_expenses
        color = theme_manager.get_color("success") if net_change >= 0 else theme_manager.get_color("danger")
        self.create_summary_card(
            cards_frame,
            "📈 Net Change",
            f"${net_change:.2f}",
            color,
            2
        )
        
        # Goals progress
        completed_goals = sum(1 for goal in self.goals if goal.is_completed)
        self.create_summary_card(
            cards_frame,
            "🎯 Goals Met",
            f"{completed_goals}/{len(self.goals)}",
            theme_manager.get_color("info"),
            3
        )
    
    def create_summary_card(self, parent, title: str, value: str, color: str, column: int):
        """Create an individual summary card."""
        card = ctk.CTkFrame(parent, **theme_manager.get_card_style())
        card.grid(row=0, column=column, sticky="ew", padx=5, pady=5)
        
        # Title
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=theme_manager.get_color("text_secondary")
        )
        title_label.pack(pady=(15, 5))
        
        # Value
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=color
        )
        value_label.pack(pady=(0, 15))
    
    def create_activity_section(self):
        """Create the activity and charts section."""
        activity_frame = ctk.CTkFrame(self, fg_color="transparent")
        activity_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
        activity_frame.grid_columnconfigure((0, 1), weight=1)
        activity_frame.grid_rowconfigure(0, weight=1)
        
        # Recent transactions
        self.create_recent_transactions(activity_frame)
        
        # Goals progress
        self.create_goals_progress(activity_frame)
    
    def create_recent_transactions(self, parent):
        """Create recent transactions list."""
        trans_frame = ctk.CTkFrame(parent)
        trans_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        trans_frame.grid_columnconfigure(0, weight=1)
        trans_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            trans_frame,
            text="Recent Transactions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header_label.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        # Scrollable list
        scrollable = ctk.CTkScrollableFrame(trans_frame)
        scrollable.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        # Combine and sort transactions
        all_transactions = []
        
        for expense in self.expenses[-10:]:  # Last 10 expenses
            all_transactions.append({
                'type': 'expense',
                'amount': -expense.amount,
                'description': expense.description,
                'date': expense.date,
                'category': self.get_category_name(expense.category_id)
            })
        
        for saving in self.savings[-10:]:  # Last 10 savings
            all_transactions.append({
                'type': 'savings',
                'amount': saving.amount,
                'description': saving.description,
                'date': saving.date,
                'category': self.get_category_name(saving.category_id)
            })
        
        # Sort by date (newest first)
        all_transactions.sort(key=lambda x: x['date'], reverse=True)
        
        if not all_transactions:
            empty_label = ctk.CTkLabel(
                scrollable,
                text="No transactions this month",
                font=ctk.CTkFont(size=14),
                text_color=theme_manager.get_color("text_secondary")
            )
            empty_label.pack(pady=20)
        else:
            for trans in all_transactions[:10]:  # Show top 10
                self.create_transaction_item(scrollable, trans)
    
    def create_transaction_item(self, parent, transaction: Dict):
        """Create a transaction item."""
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", pady=2, padx=5)
        
        # Icon and type
        icon = "💸" if transaction['type'] == 'expense' else "💰"
        color = theme_manager.get_color("danger") if transaction['amount'] < 0 else theme_manager.get_color("success")
        
        # Left side - icon and description
        left_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True)
        
        desc_label = ctk.CTkLabel(
            left_frame,
            text=f"{icon} {transaction['description']}",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        desc_label.pack(anchor="w")
        
        detail_label = ctk.CTkLabel(
            left_frame,
            text=f"{transaction['category']} • {transaction['date'].strftime('%m/%d')}",
            font=ctk.CTkFont(size=10),
            text_color=theme_manager.get_color("text_secondary"),
            anchor="w"
        )
        detail_label.pack(anchor="w")
        
        # Right side - amount
        amount_label = ctk.CTkLabel(
            item_frame,
            text=f"${abs(transaction['amount']):.2f}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=color
        )
        amount_label.pack(side="right", padx=(10, 0))
    
    def create_goals_progress(self, parent):
        """Create goals progress section."""
        goals_frame = ctk.CTkFrame(parent)
        goals_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        goals_frame.grid_columnconfigure(0, weight=1)
        goals_frame.grid_rowconfigure(1, weight=1)
        
        # Header
        header_label = ctk.CTkLabel(
            goals_frame,
            text="Goals Progress",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header_label.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        # Scrollable goals list
        scrollable = ctk.CTkScrollableFrame(goals_frame)
        scrollable.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        
        if not self.goals:
            empty_label = ctk.CTkLabel(
                scrollable,
                text="No goals set yet\nCreate your first goal!",
                font=ctk.CTkFont(size=14),
                text_color=theme_manager.get_color("text_secondary")
            )
            empty_label.pack(pady=20)
        else:
            for goal in self.goals[:5]:  # Show top 5 goals
                self.create_goal_item(scrollable, goal)
    
    def create_goal_item(self, parent, goal: Goal):
        """Create a goal progress item."""
        item_frame = ctk.CTkFrame(parent, fg_color="transparent")
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Goal name
        name_label = ctk.CTkLabel(
            item_frame,
            text=goal.name,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        name_label.pack(anchor="w")
        
        # Progress bar
        progress = min(goal.progress_percentage / 100, 1.0)
        progress_bar = ctk.CTkProgressBar(item_frame, width=200, height=8)
        progress_bar.pack(fill="x", pady=(5, 2))
        progress_bar.set(progress)
        
        # Progress text
        progress_text = f"${goal.current_amount:.0f} / ${goal.target_amount:.0f} ({goal.progress_percentage:.1f}%)"
        progress_label = ctk.CTkLabel(
            item_frame,
            text=progress_text,
            font=ctk.CTkFont(size=10),
            text_color=theme_manager.get_color("text_secondary"),
            anchor="w"
        )
        progress_label.pack(anchor="w")
    
    def get_category_name(self, category_id: int) -> str:
        """Get category name by ID."""
        if not category_id:
            return "Unknown"
        
        category = next((cat for cat in self.categories if cat.id == category_id), None)
        return category.name if category else "Unknown"
    
    def previous_month(self):
        """Navigate to previous month."""
        self.current_month = (self.current_month - timedelta(days=1)).replace(day=1)
        self.month_label.configure(text=self.current_month.strftime("%B %Y"))
        self.refresh_data()
    
    def next_month(self):
        """Navigate to next month."""
        next_month_date = self.current_month + timedelta(days=32)
        self.current_month = next_month_date.replace(day=1)
        self.month_label.configure(text=self.current_month.strftime("%B %Y"))
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh all data and update interface."""
        self.load_data()
        
        # Clear and recreate interface
        for widget in self.winfo_children():
            widget.destroy()
        
        self.create_interface()