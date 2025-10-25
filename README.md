# 💰 Smart Expense Tracker (Indian Rupees)

A comprehensive Python-based web application for tracking, categorizing, visualizing, and analyzing daily expenses in Indian Rupees (₹) with predictive insights and budget alerts.

## 🚀 Features

- **📊 Interactive Dashboard**: Real-time overview of your spending with key metrics in ₹
- **➕ Expense Management**: Easy-to-use interface for adding, viewing, and managing expenses
- **📈 Advanced Analytics**: Interactive charts and visualizations using Plotly
- **💰 Budget Management**: Set category-wise budgets with overspending alerts
- **🤖 AI-Powered Insights**: Smart recommendations and spending pattern analysis
- **📄 Report Generation**: Export detailed reports in Excel and PDF formats
- **🔮 Predictive Analytics**: Linear Regression model to predict next month's spending
- **🔄 Real-time Updates**: Automatic refresh and data synchronization
- **📱 Mobile Responsive**: Works perfectly on desktop and mobile devices

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **Frontend**: Streamlit
- **Database**: CSV (local storage) with robust date handling
- **Visualization**: Plotly with interactive charts
- **Machine Learning**: scikit-learn for Linear Regression
- **Export**: openpyxl (Excel), reportlab (PDF)
- **Currency**: Indian Rupees (₹) with proper formatting
- **Data Processing**: Pandas with error-resistant operations

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SmartExpenseTracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   # Recommended method
   python -m streamlit run app.py
   
   # Alternative methods
   python app.py
   # or use the provided scripts
   run_app.bat        # Windows
   .\run_app.ps1      # PowerShell
   ```

4. **Open your browser**
   Navigate to the URL shown in the terminal (usually `http://localhost:8501`)

## 🎯 Usage

### Getting Started
1. **Launch the app** using `python -m streamlit run app.py`
2. **Start with zero rupees** - Clean slate for expense tracking
3. **Add your first expense** using the "Add Expense" page

### Adding Expenses
1. Go to "Add Expense" page
2. Fill in the date, category, amount (in ₹), and description
3. Click "Add Expense" to save
4. Use the refresh button on dashboard if data doesn't appear immediately

### Setting Budgets
1. Navigate to "Budget Management"
2. Select a category and set the budget amount (in ₹)
3. Monitor budget vs actual spending with visual alerts

### Viewing Analytics
1. Use the "Analytics" page to see spending trends
2. Analyze category-wise spending patterns
3. Get predictions for next month's spending
4. View interactive charts and visualizations

### Generating Reports
1. Go to "Reports" page
2. Select the date range
3. Export data in Excel or PDF format with ₹ currency

## 📊 Key Features Explained

### Dashboard
- Real-time expense overview in Indian Rupees (₹)
- Monthly spending metrics with key statistics
- Budget alerts for overspending with visual indicators
- Interactive charts and visualizations
- Refresh button for real-time data updates

### Budget Management
- Set category-wise monthly budgets in ₹
- Track budget vs actual spending with progress indicators
- Visual alerts for overspending with detailed breakdowns
- Budget utilization charts and comparisons

### Analytics
- Monthly spending trends with interactive line charts
- Category-wise analysis with bar charts
- Top expenses tracking with detailed breakdowns
- Predictive spending forecasts using Linear Regression

### AI Insights
- Spending pattern analysis with trend detection
- Smart recommendations for budget optimization
- Consistency tracking across months
- Category optimization tips and alerts

## 🔧 Configuration

### Currency Settings
The application is configured for Indian Rupees (₹) by default:
- All amounts displayed in ₹
- Budget amounts in ₹
- Export reports in ₹
- Sample data with realistic ₹ amounts

### Data Storage
- **Expenses**: Stored in `expenses.csv` with proper date formatting
- **Budgets**: Stored in `budgets.json` with category-wise amounts
- **Automatic backup**: Data is saved automatically after each operation

### Optional: OpenAI Integration
To enable enhanced AI-powered insights, add your OpenAI API key:

1. Create a `.env` file in the project root
2. Add: `OPENAI_API_KEY=your_api_key_here`
3. Install python-dotenv: `pip install python-dotenv`

## 📁 Project Structure

```
SmartExpenseTracker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── demo.py               # Sample data generator
├── expenses.csv          # Expense data (created automatically)
├── budgets.json          # Budget data (created automatically)
├── run_app.bat          # Windows startup script
├── run_app.ps1          # PowerShell startup script
├── README.md            # Project documentation
└── QUICK_START.md       # Quick start guide
```

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your GitHub repository to Streamlit Cloud
3. Deploy with one click

### Local Development
```bash
# Recommended method
python -m streamlit run app.py

# With custom port
python -m streamlit run app.py --server.port 8501

# Using provided scripts
run_app.bat        # Windows
.\run_app.ps1      # PowerShell
```

## 📈 Future Enhancements

- [ ] Database integration (SQLite/PostgreSQL)
- [ ] User authentication and multi-user support
- [ ] Mobile app integration
- [ ] Advanced ML models for better predictions
- [ ] Integration with banking APIs
- [ ] Recurring expense tracking
- [ ] Investment tracking
- [ ] Goal-based savings tracking
- [ ] Multi-currency support
- [ ] Advanced reporting with more chart types
- [ ] Expense categorization with AI
- [ ] Receipt scanning and OCR integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

1. **Streamlit command not found**
   ```bash
   # Use this instead
   python -m streamlit run app.py
   ```

2. **Date parsing errors**
   - The app now handles date formats automatically
   - If issues persist, check your system date format

3. **Data not showing after adding expenses**
   - Use the refresh button on the dashboard
   - Check if the expense was saved successfully

4. **Port already in use**
   - The app will automatically find an available port
   - Check the terminal output for the correct URL

### Getting Help

- Check the terminal output for error messages
- Ensure all dependencies are installed correctly
- Verify Python version compatibility (3.8+)

## 🙏 Acknowledgments

- Streamlit for the amazing web framework
- Plotly for interactive visualizations
- scikit-learn for machine learning capabilities
- Pandas for robust data processing
- The open-source community for inspiration and tools

---

**Happy Expense Tracking in Indian Rupees! 💰📊🇮🇳**
