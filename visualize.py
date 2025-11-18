import sqlite3

import pandas as pd
import matplotlib.pyplot as plt


DB_PATH = "finance_warehouse.db"


def get_aapl_data():
    """Read AAPL price data from the SQLite database."""
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        dp.date,
        dp.close
    FROM daily_prices dp
    JOIN tickers t ON dp.ticker_id = t.id
    WHERE t.symbol = 'AAPL'
    ORDER BY dp.date;
    """

    df = pd.read_sql(query, conn, parse_dates=["date"])
    conn.close()
    return df


def plot_aapl(df):
    """Plot AAPL closing price over time."""
    plt.figure(figsize=(10, 5))
    plt.plot(df["date"], df["close"])

    plt.title("AAPL Closing Price Over Time")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.grid(True)
    plt.tight_layout()

    # Save the chart as an image file
    plt.savefig("aapl_price.png")
    print("Saved chart as aapl_price.png")

    # Show the chart window (optional)
    plt.show()


def main():
    df = get_aapl_data()
    print(df.head())  # just to see a sample in the terminal
    plot_aapl(df)


if __name__ == "__main__":
    main()
