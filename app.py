import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import os
import json
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import numpy as np
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import io
import base64

# Page configuration
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .alert-box {
        background-color: #ffebee;
        border: 1px solid #f44336;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e8;
        border: 1px solid #4caf50;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class ExpenseTracker:
    def __init__(self):
        self.data_file = "expenses.csv"
        self.budget_file = "budgets.json"
        self.load_data()
    
    def load_data(self):
        """Load expenses and budget data from files"""
        # Load expenses
        if os.path.exists(self.data_file):
            self.expenses_df = pd.read_csv(self.data_file)
            # Handle different date formats more flexibly
            self.expenses_df['date'] = pd.to_datetime(self.expenses_df['date'], errors='coerce')
            # Remove any rows with invalid dates
            self.expenses_df = self.expenses_df.dropna(subset=['date'])
        else:
            self.expenses_df = pd.DataFrame(columns=['date', 'category', 'amount', 'description'])
        
        # Load budgets
        if os.path.exists(self.budget_file):
            with open(self.budget_file, 'r') as f:
                self.budgets = json.load(f)
        else:
            self.budgets = {}
    
    def save_data(self):
        """Save expenses and budget data to files"""
        self.expenses_df.to_csv(self.data_file, index=False)
        with open(self.budget_file, 'w') as f:
            json.dump(self.budgets, f)
    
    def add_expense(self, date, category, amount, description):
        """Add a new expense"""
        # Convert date to string format for consistency
        if hasattr(date, 'strftime'):
            date_str = date.strftime('%Y-%m-%d')
        else:
            date_str = str(date)
            
        new_expense = pd.DataFrame({
            'date': [date_str],
            'category': [category],
            'amount': [amount],
            'description': [description]
        })
        self.expenses_df = pd.concat([self.expenses_df, new_expense], ignore_index=True)
        self.save_data()
    
    def get_categories(self):
        """Get unique categories from expenses"""
        return sorted(self.expenses_df['category'].unique().tolist()) if not self.expenses_df.empty else []
    
    def get_monthly_summary(self, year, month):
        """Get monthly expense summary"""
        monthly_data = self.expenses_df[
            (self.expenses_df['date'].dt.year == year) & 
            (self.expenses_df['date'].dt.month == month)
        ]
        return monthly_data
    
    def get_category_totals(self, year, month):
        """Get category-wise totals for a month"""
        monthly_data = self.get_monthly_summary(year, month)
        if monthly_data.empty:
            return pd.DataFrame()
        return monthly_data.groupby('category')['amount'].sum().reset_index()
    
    def predict_next_month(self):
        """Predict next month's spending using Linear Regression"""
        if len(self.expenses_df) < 3:
            return None, "Not enough data for prediction"
        
        # Prepare data for ML model
        self.expenses_df['year'] = self.expenses_df['date'].dt.year
        self.expenses_df['month'] = self.expenses_df['date'].dt.month
        monthly_totals = self.expenses_df.groupby(['year', 'month'])['amount'].sum().reset_index()
        monthly_totals['month_num'] = monthly_totals['year'] * 12 + monthly_totals['month']
        
        if len(monthly_totals) < 3:
            return None, "Not enough monthly data for prediction"
        
        # Train model
        X = monthly_totals[['month_num']].values
        y = monthly_totals['amount'].values
        
        model = LinearRegression()
        model.fit(X, y)
        
        # Predict next month
        current_year = datetime.now().year
        current_month = datetime.now().month
        next_month_num = current_year * 12 + current_month + 1
        
        prediction = model.predict([[next_month_num]])[0]
        
        return max(0, prediction), "Prediction based on historical data"
    
    def check_budget_alerts(self, year, month):
        """Check for budget overspending alerts"""
        alerts = []
        monthly_data = self.get_monthly_summary(year, month)
        
        if monthly_data.empty:
            return alerts
        
        category_totals = self.get_category_totals(year, month)
        
        for _, row in category_totals.iterrows():
            category = row['category']
            spent = row['amount']
            budget = self.budgets.get(category, 0)
            
            if budget > 0 and spent > budget:
                overspend = spent - budget
                alerts.append({
                    'category': category,
                    'budget': budget,
                    'spent': spent,
                    'overspend': overspend
                })
        
        return alerts

def main():
    # Initialize tracker
    tracker = ExpenseTracker()
    
    # Main header
    st.markdown('<h1 class="main-header">💰 Smart Expense Tracker</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["📊 Dashboard", "➕ Add Expense", "📈 Analytics", "💰 Budget Management", "🤖 AI Insights", "📄 Reports"]
    )
    
    if page == "📊 Dashboard":
        show_dashboard(tracker)
    elif page == "➕ Add Expense":
        show_add_expense(tracker)
    elif page == "📈 Analytics":
        show_analytics(tracker)
    elif page == "💰 Budget Management":
        show_budget_management(tracker)
    elif page == "🤖 AI Insights":
        show_ai_insights(tracker)
    elif page == "📄 Reports":
        show_reports(tracker)

def show_dashboard(tracker):
    """Display the main dashboard"""
    st.header("📊 Expense Dashboard")
    
    # Refresh button
    if st.button("🔄 Refresh Data", type="secondary"):
        st.rerun()
    
    # Date selection
    col1, col2 = st.columns(2)
    with col1:
        selected_year = st.selectbox("Select Year", range(2020, datetime.now().year + 2), index=datetime.now().year - 2020)
    with col2:
        selected_month = st.selectbox("Select Month", range(1, 13), index=datetime.now().month - 1)
    
    # Get monthly data
    monthly_data = tracker.get_monthly_summary(selected_year, selected_month)
    
    if monthly_data.empty:
        st.info("📝 No expenses found for the selected month. Add some expenses using the 'Add Expense' page!")
        st.markdown("---")
        st.markdown("### 💡 Quick Start")
        st.markdown("1. Go to **Add Expense** page")
        st.markdown("2. Fill in the expense details")
        st.markdown("3. Click **Add Expense** to save")
        st.markdown("4. Return to **Dashboard** to see your data")
        return
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spent = monthly_data['amount'].sum()
        st.metric("Total Spent", f"₹{total_spent:,.2f}")
    
    with col2:
        avg_daily = total_spent / len(monthly_data['date'].dt.day.unique())
        st.metric("Avg Daily", f"₹{avg_daily:,.2f}")
    
    with col3:
        num_transactions = len(monthly_data)
        st.metric("Transactions", num_transactions)
    
    with col4:
        top_category = monthly_data.groupby('category')['amount'].sum().idxmax()
        st.metric("Top Category", top_category)
    
    # Budget alerts
    alerts = tracker.check_budget_alerts(selected_year, selected_month)
    if alerts:
        st.markdown('<div class="alert-box">', unsafe_allow_html=True)
        st.error("🚨 Budget Alerts!")
        for alert in alerts:
            st.write(f"**{alert['category']}**: Spent ₹{alert['spent']:,.2f} (Budget: ₹{alert['budget']:,.2f}) - Overspent by ₹{alert['overspend']:,.2f}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Category breakdown
        category_totals = tracker.get_category_totals(selected_year, selected_month)
        if not category_totals.empty:
            fig = px.pie(category_totals, values='amount', names='category', title="Expenses by Category")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Daily spending trend
        daily_totals = monthly_data.groupby(monthly_data['date'].dt.day)['amount'].sum().reset_index()
        daily_totals.columns = ['day', 'amount']
        fig = px.line(daily_totals, x='day', y='amount', title="Daily Spending Trend")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent transactions
    st.subheader("Recent Transactions")
    recent_expenses = monthly_data.sort_values('date', ascending=False).head(10)
    st.dataframe(recent_expenses, use_container_width=True)

def show_add_expense(tracker):
    """Show add expense form"""
    st.header("➕ Add New Expense")
    
    with st.form("add_expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            expense_date = st.date_input("Date", value=date.today())
            category = st.selectbox("Category", [
                "Food & Dining", "Transportation", "Shopping", "Entertainment", 
                "Bills & Utilities", "Healthcare", "Education", "Travel", "Other"
            ])
        
        with col2:
            amount = st.number_input("Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
            description = st.text_input("Description")
        
        submitted = st.form_submit_button("Add Expense", type="primary")
        
        if submitted:
            if amount > 0 and description:
                tracker.add_expense(expense_date, category, amount, description)
                st.success("✅ Expense added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields with valid values.")

def show_analytics(tracker):
    """Show analytics and visualizations"""
    st.header("📈 Analytics & Insights")
    
    if tracker.expenses_df.empty:
        st.warning("No expense data available for analytics.")
        return
    
    # Time period selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=tracker.expenses_df['date'].min().date())
    with col2:
        end_date = st.date_input("End Date", value=tracker.expenses_df['date'].max().date())
    
    # Filter data
    filtered_data = tracker.expenses_df[
        (tracker.expenses_df['date'].dt.date >= start_date) & 
        (tracker.expenses_df['date'].dt.date <= end_date)
    ]
    
    if filtered_data.empty:
        st.warning("No data available for the selected period.")
        return
    
    # Spending trends
    st.subheader("Spending Trends")
    
    # Monthly spending
    filtered_data['year'] = filtered_data['date'].dt.year
    filtered_data['month'] = filtered_data['date'].dt.month
    monthly_spending = filtered_data.groupby(['year', 'month'])['amount'].sum().reset_index()
    monthly_spending['month_year'] = monthly_spending['year'].astype(str) + '-' + monthly_spending['month'].astype(str)
    
    fig = px.line(monthly_spending, x='month_year', y='amount', title="Monthly Spending Trend")
    st.plotly_chart(fig, use_container_width=True)
    
    # Category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        category_totals = filtered_data.groupby('category')['amount'].sum().sort_values(ascending=False)
        fig = px.bar(x=category_totals.index, y=category_totals.values, title="Spending by Category")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top expenses
        top_expenses = filtered_data.nlargest(10, 'amount')
        fig = px.bar(top_expenses, x='description', y='amount', title="Top 10 Expenses")
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Prediction
    st.subheader("Next Month Prediction")
    prediction, message = tracker.predict_next_month()
    if prediction is not None:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Predicted Spending", f"₹{prediction:,.2f}")
        with col2:
            st.info(f"ℹ️ {message}")
    else:
        st.warning(message)

def show_budget_management(tracker):
    """Show budget management interface"""
    st.header("💰 Budget Management")
    
    # Current budgets
    st.subheader("Current Budgets")
    
    if tracker.budgets:
        budget_df = pd.DataFrame(list(tracker.budgets.items()), columns=['Category', 'Budget Amount'])
        st.dataframe(budget_df, use_container_width=True)
    else:
        st.info("No budgets set yet.")
    
    # Add/Edit budget
    st.subheader("Set Budget")
    
    with st.form("budget_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            category = st.selectbox("Category", [
                "Food & Dining", "Transportation", "Shopping", "Entertainment", 
                "Bills & Utilities", "Healthcare", "Education", "Travel", "Other"
            ])
        
        with col2:
            budget_amount = st.number_input("Budget Amount (₹)", min_value=0.01, step=0.01, format="%.2f")
        
        submitted = st.form_submit_button("Set Budget", type="primary")
        
        if submitted:
            tracker.budgets[category] = budget_amount
            tracker.save_data()
            st.success(f"✅ Budget set for {category}: ₹{budget_amount:,.2f}")
            st.rerun()
    
    # Budget vs Actual
    if tracker.budgets:
        st.subheader("Budget vs Actual (Current Month)")
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        budget_comparison = []
        for category, budget in tracker.budgets.items():
            monthly_data = tracker.get_monthly_summary(current_year, current_month)
            if not monthly_data.empty:
                spent = monthly_data[monthly_data['category'] == category]['amount'].sum()
            else:
                spent = 0
            
            budget_comparison.append({
                'Category': category,
                'Budget': budget,
                'Spent': spent,
                'Remaining': budget - spent,
                'Percentage': (spent / budget * 100) if budget > 0 else 0
            })
        
        if budget_comparison:
            comparison_df = pd.DataFrame(budget_comparison)
            st.dataframe(comparison_df, use_container_width=True)
            
            # Budget utilization chart
            fig = px.bar(comparison_df, x='Category', y=['Budget', 'Spent'], 
                        title="Budget vs Actual Spending", barmode='group')
            st.plotly_chart(fig, use_container_width=True)

def show_ai_insights(tracker):
    """Show AI-powered insights"""
    st.header("🤖 AI-Powered Financial Insights")
    
    if tracker.expenses_df.empty:
        st.warning("No expense data available for AI analysis.")
        return
    
    # Basic insights without OpenAI API
    st.subheader("Smart Insights")
    
    # Spending patterns
    tracker.expenses_df['year'] = tracker.expenses_df['date'].dt.year
    tracker.expenses_df['month'] = tracker.expenses_df['date'].dt.month
    monthly_totals = tracker.expenses_df.groupby(['year', 'month'])['amount'].sum()
    
    if len(monthly_totals) >= 2:
        recent_avg = monthly_totals.tail(3).mean()
        previous_avg = monthly_totals.head(-3).mean() if len(monthly_totals) > 3 else monthly_totals.iloc[0]
        
        change_percent = ((recent_avg - previous_avg) / previous_avg) * 100
        
        if change_percent > 10:
            st.warning(f"📈 Your spending has increased by {change_percent:.1f}% recently. Consider reviewing your expenses.")
        elif change_percent < -10:
            st.success(f"📉 Great job! Your spending has decreased by {abs(change_percent):.1f}% recently.")
        else:
            st.info(f"📊 Your spending has been relatively stable with a {change_percent:.1f}% change.")
    
    # Category insights
    category_totals = tracker.expenses_df.groupby('category')['amount'].sum().sort_values(ascending=False)
    
    st.subheader("Category Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top Spending Categories:**")
        for i, (category, amount) in enumerate(category_totals.head(3).items(), 1):
            st.write(f"{i}. {category}: ₹{amount:,.2f}")
    
    with col2:
        st.write("**Spending Distribution:**")
        total_spent = category_totals.sum()
        for category, amount in category_totals.head(3).items():
            percentage = (amount / total_spent) * 100
            st.write(f"{category}: {percentage:.1f}%")
    
    # Recommendations
    st.subheader("💡 Recommendations")
    
    # Find highest spending category
    top_category = category_totals.index[0]
    top_amount = category_totals.iloc[0]
    
    st.write(f"• **Focus on {top_category}**: You've spent ₹{top_amount:,.2f} in this category. Consider setting a budget or finding ways to reduce costs.")
    
    # Check for frequent small expenses
    small_expenses = tracker.expenses_df[tracker.expenses_df['amount'] < 100]
    if len(small_expenses) > 10:
        small_total = small_expenses['amount'].sum()
        st.write(f"• **Small expenses add up**: You have {len(small_expenses)} small expenses totaling ₹{small_total:,.2f}. Consider tracking these more carefully.")
    
    # Monthly consistency
    if len(monthly_totals) >= 3:
        monthly_std = monthly_totals.std()
        monthly_mean = monthly_totals.mean()
        cv = monthly_std / monthly_mean
        
        if cv > 0.3:
            st.write("• **Inconsistent spending**: Your monthly spending varies significantly. Try to maintain more consistent spending patterns.")
        else:
            st.write("• **Consistent spending**: Great job maintaining consistent monthly spending patterns!")

def show_reports(tracker):
    """Show reports and export options"""
    st.header("📄 Reports & Export")
    
    if tracker.expenses_df.empty:
        st.warning("No expense data available for reports.")
        return
    
    # Report period selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Report Start Date", value=tracker.expenses_df['date'].min().date())
    with col2:
        end_date = st.date_input("Report End Date", value=tracker.expenses_df['date'].max().date())
    
    # Filter data
    filtered_data = tracker.expenses_df[
        (tracker.expenses_df['date'].dt.date >= start_date) & 
        (tracker.expenses_df['date'].dt.date <= end_date)
    ]
    
    if filtered_data.empty:
        st.warning("No data available for the selected period.")
        return
    
    # Summary statistics
    st.subheader("Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_spent = filtered_data['amount'].sum()
        st.metric("Total Spent", f"₹{total_spent:,.2f}")
    
    with col2:
        avg_expense = filtered_data['amount'].mean()
        st.metric("Average Expense", f"₹{avg_expense:,.2f}")
    
    with col3:
        num_transactions = len(filtered_data)
        st.metric("Total Transactions", num_transactions)
    
    with col4:
        unique_categories = filtered_data['category'].nunique()
        st.metric("Categories Used", unique_categories)
    
    # Category breakdown
    st.subheader("Category Breakdown")
    category_summary = filtered_data.groupby('category').agg({
        'amount': ['sum', 'count', 'mean']
    }).round(2)
    category_summary.columns = ['Total Amount', 'Count', 'Average']
    st.dataframe(category_summary, use_container_width=True)
    
    # Export options
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📊 Export to Excel", type="primary"):
            # Create Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_data.to_excel(writer, sheet_name='Expenses', index=False)
                category_summary.to_excel(writer, sheet_name='Category Summary')
            
            output.seek(0)
            b64 = base64.b64encode(output.read()).decode()
            href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="expense_report.xlsx">Download Excel Report</a>'
            st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        if st.button("📄 Export to PDF", type="primary"):
            # Create PDF report
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Title
            title = Paragraph("Expense Report", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Summary
            summary_text = f"""
            <b>Report Period:</b> {start_date} to {end_date}<br/>
            <b>Total Spent:</b> ₹{total_spent:,.2f}<br/>
            <b>Total Transactions:</b> {num_transactions}<br/>
            <b>Average Expense:</b> ₹{avg_expense:,.2f}
            """
            summary = Paragraph(summary_text, styles['Normal'])
            story.append(summary)
            story.append(Spacer(1, 12))
            
            # Category table
            story.append(Paragraph("Category Breakdown", styles['Heading2']))
            table_data = [['Category', 'Total Amount', 'Count', 'Average']]
            for category, row in category_summary.iterrows():
                table_data.append([
                    category,
                    f"₹{row['Total Amount']:,.2f}",
                    str(row['Count']),
                    f"₹{row['Average']:,.2f}"
                ])
            
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(table)
            
            doc.build(story)
            buffer.seek(0)
            
            b64 = base64.b64encode(buffer.read()).decode()
            href = f'<a href="data:application/pdf;base64,{b64}" download="expense_report.pdf">Download PDF Report</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
