📊 Financial Data Warehouse & Analytics Pipeline

This project builds a complete end-to-end financial data pipeline using Python, SQL, and data visualization tools.
It downloads historical stock price data, stores it in a SQL database, and generates visual analytics from the stored data.

🚀 Project Features
1. Automated Data Pipeline (ETL)

Downloads historical stock price data using yfinance

Cleans and transforms the data with pandas

Stores data in a SQLite database using SQL scripts

Handles ticker insertion and daily price ingestion

2. SQL Data Warehouse

Custom database schema:

tickers (list of stock symbols)

daily_prices (full historical OHLCV data)

Supports scalable storage for multiple tickers

Easy to query using SQL or Python

3. Stock Price Visualization

Reads stored data directly from SQLite

Generates clean line charts using matplotlib

Saves plots as .png files for dashboards or presentations

Example visual: AAPL closing price chart

🛠 Tech Stack

Languages: Python, SQL
Libraries: pandas, yfinance, matplotlib, sqlite3
Database: SQLite
Tools: VS Code

📁 Project Structure
finance-data-warehouse/
│
├── etl.py              # Extract, Transform, Load (ETL) pipeline
├── visualize.py        # Visualization script (matplotlib)
├── schema.sql          # SQL database schema
├── finance_warehouse.db # SQLite database file (auto-generated)
├── aapl_price.png      # Sample chart generated from DB
└── README.md           # Documentation

📈 Example Output

Below is an example visualization generated from this project:

AAPL Closing Price (2018–Present)


🧠 How It Works

Run the ETL script:

python3 etl.py


Creates the database and tables

Downloads stock data

Inserts it into SQLite

Generate the visualization:

python3 visualize.py


Reads data from SQLite

Creates and saves the chart

🔮 Future Improvements

Add multiple tickers (MSFT, AMZN, GOOGL, META)

Add daily returns and volatility calculations

Build a Tableau / Power BI dashboard

Add a portfolio optimizer using Python

Schedule daily automatic updates

📝 Author

Mannat Sadana
Finance + Computational Data Science Student
Passionate about data engineering, analytics, and financial modeling.