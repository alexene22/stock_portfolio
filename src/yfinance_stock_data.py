"""
This module provides functions to fetch stock prices and validate ticker symbols using the yfinance library.
"""

import yfinance as yf


def get_ticker_price(symbol: str) -> float:
    """
    This function uses the yfinance library to retrieve the current stock price.

    Args:
        symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
    Returns:
        float: The current stock price, or None if the symbol is invalid or data cannot be fetched.
    """
    try:
        stock = yf.Ticker(symbol)  # Refresh every minute
        history = stock.history(period="1d")
        if history.empty or "Close" not in history.columns:
            raise ValueError(f"No data available for ticker {symbol}")
        price = history["Close"].iloc[-1]
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError(f"Invalid price data for ticker {symbol}")
        return price
    except Exception as e:
        raise ValueError(f"Failed to fetch price for {symbol}: {e}")


def main():
    """Main function to run the stock price retrieval."""
    symbol = input("Enter stock ticker (e.g. AAPL, MSFT): ").strip().upper()
    price = get_ticker_price(symbol)
    if price is not None:
        print(f"The current price of {symbol} is ${price:.2f}")
    else:
        print(
            f"Could not retrieve price for {symbol}. Please check the ticker symbol and try again."
        )


if __name__ == "__main__":
    main()
