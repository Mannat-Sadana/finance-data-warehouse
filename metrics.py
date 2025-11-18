import sqlite3

import pandas as pd


DB_PATH = "finance_warehouse.db"


def get_price_data(symbol="AAPL"):
    """Read price data for one ticker from the SQLite database."""
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
    return df


def add_return_metrics(df):
    """Add daily return and rolling metrics."""
    # Sort just to be safe
    df = df.sort_values("date").reset_index(drop=True)

    # Simple daily return: (P_t - P_{t-1}) / P_{t-1}
    df["daily_return"] = df["close"].pct_change()

    # Rolling 20-day average return (about 1 trading month)
    df["rolling_20d_return"] = df["daily_return"].rolling(window=20).mean()

    # Rolling 20-day volatility (standard deviation of daily returns)
    df["rolling_20d_volatility"] = df["daily_return"].rolling(window=20).std()

    return df


def main():
    symbol = "AAPL"  # you can change this later

    print(f"Loading price data for {symbol}...")
    df = get_price_data(symbol)

    print(f"Loaded {len(df)} rows. Adding return metrics...")
    df_with_metrics = add_return_metrics(df)

    # Show the first few rows with metrics
    print(df_with_metrics.head(15))

    # Save to CSV so you can open in Excel / Numbers
    output_file = f"{symbol.lower()}_returns_metrics.csv"
    df_with_metrics.to_csv(output_file, index=False)
    print(f"Saved metrics to {output_file}")


if __name__ == "__main__":
    main()
