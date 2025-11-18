import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "finance_warehouse.db"


def get_returns(symbol="AAPL"):
    """Load price data from DB and compute daily returns."""
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        t.symbol,
        dp.date,
        dp.close
    FROM daily_prices dp
    JOIN tickers t ON dp.ticker_id = t.id
    WHERE t.symbol = ?
    ORDER BY dp.date;
    """

    df = pd.read_sql(query, conn, params=[symbol], parse_dates=["date"])
    conn.close()

    df = df.sort_values("date").reset_index(drop=True)

    # Calculate daily returns
    df["daily_return"] = df["close"].pct_change()

    return df


def plot_daily_returns(df, symbol="AAPL"):
    """Plot the daily returns."""
    plt.figure(figsize=(12, 5))
    plt.plot(df["date"], df["daily_return"], alpha=0.7)

    plt.title(f"{symbol} Daily Returns Over Time")
    plt.xlabel("Date")
    plt.ylabel("Daily Return")
    plt.grid(True)
    plt.tight_layout()

    # Save the plot
    filename = f"{symbol.lower()}_daily_returns.png"
    plt.savefig(filename)
    print(f"Saved chart as {filename}")

    # Display the chart window
    plt.show()


def main():
    symbol = "AAPL"  # You can change this to MSFT, AMZN, etc.
    df = get_returns(symbol)

    print(df.head())  # Show the first few rows
    plot_daily_returns(df, symbol)


if __name__ == "__main__":
    main()
