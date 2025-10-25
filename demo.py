#!/usr/bin/env python3
"""
Demo script to test the Smart Expense Tracker application
This script adds some sample data to demonstrate the app's features
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample expense data for demonstration"""
    
    # Sample categories
    categories = [
        "Food & Dining", "Transportation", "Shopping", "Entertainment", 
        "Bills & Utilities", "Healthcare", "Education", "Travel", "Other"
    ]
    
    # Sample descriptions
    descriptions = {
        "Food & Dining": ["Lunch at restaurant", "Grocery shopping", "Coffee", "Dinner with friends", "Fast food"],
        "Transportation": ["Gas", "Uber ride", "Public transport", "Car maintenance", "Parking"],
        "Shopping": ["Clothes", "Electronics", "Books", "Gifts", "Household items"],
        "Entertainment": ["Movie tickets", "Concert", "Streaming service", "Games", "Sports event"],
        "Bills & Utilities": ["Electricity bill", "Internet", "Phone bill", "Water bill", "Insurance"],
        "Healthcare": ["Doctor visit", "Medicine", "Gym membership", "Dental checkup", "Vitamins"],
        "Education": ["Online course", "Books", "Software license", "Conference", "Training"],
        "Travel": ["Flight ticket", "Hotel", "Rental car", "Sightseeing", "Restaurant"],
        "Other": ["Miscellaneous", "Emergency fund", "Investment", "Donation", "Repair"]
    }
    
    # Generate sample data for the last 3 months
    expenses = []
    start_date = datetime.now() - timedelta(days=90)
    
    for i in range(100):  # Generate 100 sample expenses
        date = start_date + timedelta(days=random.randint(0, 90))
        category = random.choice(categories)
        amount = round(random.uniform(50, 5000), 2)
        description = random.choice(descriptions[category])
        
        expenses.append({
            'date': date.strftime('%Y-%m-%d'),
            'category': category,
            'amount': amount,
            'description': description
        })
    
    return pd.DataFrame(expenses)

def create_sample_budgets():
    """Create sample budget data in Indian Rupees"""
    return {
        "Food & Dining": 8000.0,
        "Transportation": 3000.0,
        "Shopping": 5000.0,
        "Entertainment": 2000.0,
        "Bills & Utilities": 4000.0,
        "Healthcare": 1500.0,
        "Education": 1000.0,
        "Travel": 3000.0,
        "Other": 2000.0
    }

if __name__ == "__main__":
    print("Creating sample data for Smart Expense Tracker...")
    
    # Create sample expenses
    expenses_df = create_sample_data()
    expenses_df.to_csv("expenses.csv", index=False)
    print(f"Created {len(expenses_df)} sample expenses")
    
    # Create sample budgets
    import json
    budgets = create_sample_budgets()
    with open("budgets.json", "w") as f:
        json.dump(budgets, f)
    print("Created sample budgets")
    
    print("\nSample data created successfully!")
    print("Now you can run: streamlit run app.py")
    print("The app will have sample data to demonstrate all features.")
