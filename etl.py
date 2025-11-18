import sqlite3
import datetime as dt

import pandas as pd
import yfinance as yf


DB_PATH = "finance_warehouse.db"


def create_tables():
    """Create the SQLite database and tables from schema.sql"""
    conn = sqlite3.connect(DB_PATH)

    with open("schema.sql") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    return conn


def insert_tickers(conn, symbols):
    """Insert ticker symbols into the tickers table (ignore duplicates)."""
    cur = conn.cursor()
    for symbol in symbols:
        cur.execute(
            "INSERT OR IGNORE INTO tickers (symbol) VALUES (?)",
            (symbol,),
        )
    conn.commit()


def load_prices_for_ticker(conn, symbol, start="2018-01-01"):
    """Download price history for one ticker and load into daily_prices."""
    end = dt.date.today().isoformat()

    print(f"Downloading data for {symbol} from {start} to {end}...")
    # Force yfinance to return standard OHLCV columns
    df = yf.download(symbol, start=start, end=end, auto_adjust=False)

    if df.empty:
        print(f"No data returned for {symbol}")
        return

    # If yfinance returns a MultiIndex for columns, flatten it
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # Reset index so Date becomes a column
    df.reset_index(inplace=True)

    # Rename columns to match our table names
    df.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adj_close",
            "Volume": "volume",
        },
        inplace=True,
    )

    # Look up ticker_id from tickers table
    cur = conn.cursor()
    cur.execute("SELECT id FROM tickers WHERE symbol = ?", (symbol,))
    row = cur.fetchone()

    if row is None:
        print(f"Could not find ticker_id for {symbol} in tickers table.")
        return

    ticker_id = row[0]
    df["ticker_id"] = ticker_id

    # Remove existing rows for this ticker so we don't duplicate on rerun
    cur.execute("DELETE FROM daily_prices WHERE ticker_id = ?", (ticker_id,))
    conn.commit()

    # Keep only the columns that match daily_prices, and flatten column names
    df = df[
        [
            "ticker_id",
            "date",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]
    ].copy()

    df.columns = [
        "ticker_id",
        "date",
        "open",
        "high",
        "low",
        "close",
        "adj_close",
        "volume",
    ]

    # Write into the daily_prices table
    df.to_sql("daily_prices", conn, if_exists="append", index=False)
    print(f"Loaded {len(df)} rows for {symbol} into daily_prices.")


def main():
    # A: create DB + tables and get a connection
    conn = create_tables()

    # B: Tickers you care about (you can add more later)
    symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "META"]

    # C: insert tickers
    insert_tickers(conn, symbols)

    # D: load prices for each ticker
    for symbol in symbols:
        load_prices_for_ticker(conn, symbol)

    conn.close()
    print("All done!")


if __name__ == "__main__":
    main()
