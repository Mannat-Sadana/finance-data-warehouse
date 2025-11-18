import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "finance_warehouse.db"


def get_returns(symbol="AAPL"):
    """Load price data and compute daily returns."""
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
    df["daily_return"] = df["close"].pct_change()

    # rolling 20-day volatility (std of daily returns)
    df["rolling_volatility"] = df["daily_return"].rolling(window=20).std()

    return df


def plot_volatility(df, symbol="AAPL"):
    """Plot the 20-day rolling volatility."""
    plt.figure(figsize=(12, 5))
    plt.plot(df["date"], df["rolling_volatility"], color="red", linewidth=1)

    plt.title(f"{symbol} 20-Day Rolling Volatility")
    plt.xlabel("Date")
    plt.ylabel("Volatility (Std Dev of Returns)")
    plt.grid(True)
    plt.tight_layout()

    filename = f"{symbol.lower()}_volatility.png"
    plt.savefig(filename)
    print(f"Saved chart as {filename}")

    plt.show()


def main():
    symbol = "AAPL"  # change later if you want
    df = get_returns(symbol)

    print(df.head(25))  # shows the first values + NaNs
    plot_volatility(df, symbol)


if __name__ == "__main__":
    main()
