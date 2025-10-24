# smart-expense-tracker
# Project Overview
A Python-based web app to track, categorize, visualize, and analyze daily expenses, helping users manage personal finances efficiently with predictive insights and budget alerts.
# Problem Statement
Many individuals struggle to track their daily spending, plan budgets, and understand their financial habits.
 * This project provides a Smart Expense Tracker that records expenses, shows spending trends, predicts future expenses, and alerts users when budgets are exceeded.
# Solution Summary 
Built a Streamlit-based web app where users can:
 * Add expenses with date, category, amount, and description
 * View expenses in tabular and graphical formats
 * Track monthly budgets with alerts for overspending
 * Predict next month’s spending using Linear Regression
 * Export reports in Excel or PDF
# Tech Stack
 * Backend: Python
 * Frontend: Streamlit
 * Database: CSV (local) or SQLite (optional)
 * Visualization: Plotly / Matplotlib
 * Machine Learning: scikit-learn
 * LLM / AI Models: OpenAI GPT API (optional for text-based insights)
 * Deployment: Streamlit Cloud / Render (optional)
 * Version Control: Git + GitHub
# Project Structure
smart_expense_tracker/
├── app.py                 # Main Streamlit app
├── expenses.csv           # Sample data storage
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── demo_video_link.txt    # Optional demo link
└── exported_reports/      # Folder for Excel / PDF outputs
# Setup Instructions (with Conda)

# 1. Clone the repository
git clone https://github.com/BOSS-script/smart-expense-tracker.git
cd smart-expense-tracker
# 2. Create and activate a conda environment
conda create -n smarttracker python=3.10 -y
conda activate smarttracker
# 3. Install dependencies
pip install -r requirements.txt
# 4. Run the app
streamlit run app.py
# Deployment
Not done yet 
# Demo Video
Not done yet 
# Features
 * End-to-end working Streamlit web app
 * Add, categorize, and visualize expenses
 * Budget alerts for overspending
 * Predictive analytics using Linear Regression
 * Export reports in Excel / PDF
 * Optional AI-powered financial insights
# Technical Architecture
Simple workflow:
 * User inputs expenses → Streamlit frontend
 * Backend logic calculates summaries and trends → Visualizations displayed
 * ML model predicts next month’s spending → Output shown to user
 * Optional: LLM generates personalized financial suggestions
# Refrences 
 * https://docs.streamlit.io/ - Streamlit Documentation
 * https://pandas.pydata.org/ - Pandas Library
 * https://plotly.com/python/ - Ploty Documentation
 * https://scikit-learn.org/stable/ - scikit-learn
