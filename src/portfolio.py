""" "
This module defines a Portfolio class that represents a stock portfolio.
"""
import json
from src.ticker import Ticker

class Portfolio:
    """
    A class to represent a stock portfolio.

    Attributes:
        cash (float): The amount of cash available in the portfolio
        tickers (list[str]): A list of stock ticker symbols in the portfolio
        _file_path: Private path to the JSON file for saving/loading portfolio data
    """

    def __init__(
        self,
        cash: float = 0.0,
        tickers: dict[str, Ticker] = None,
        file_path: str = "data/portfolio.json",
    ):
        """Initialize portfolio from JSON file or use parameters values."""
        self._file_path = file_path
        
        try:
            with open(self._file_path, "r") as f:
                data = json.load(f)
            
            self.cash = data.get("cash", cash)    
            self.tickers = {
                item["symbol"]: Ticker(symbol=item["symbol"], amount=item["amount"])
                for item in data.get("tickers", tickers if tickers is not None else {})
            }            
        except FileNotFoundError:
            self.cash = cash
            self.tickers = tickers if tickers is not None else {}
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}. Using default portfolio.")
            self.cash = cash
            self.tickers = tickers if tickers is not None else {}

    def buy_ticker(self, ticker: Ticker):
        """Add or update a Ticker object in the portfolio, deducting cost from cash."""
        if ticker.amount < 0:
            raise ValueError("Ticker amount cannot be negative")
        
        price = ticker.get_current_price()
        cost = ticker.amount * price
        if cost > self.cash:
            raise ValueError(
                f"Insufficient cash: need ${cost:.2f}, available ${self.cash:.2f}"
            )
            
        if ticker.symbol in self.tickers:
            self.tickers[
                ticker.symbol
            ].amount += ticker.amount  # Add to existing shares
        else:
            self.tickers[ticker.symbol] = ticker  # Add new ticker
            
        self.update_cash(-cost)  # Deduct cost from cash
        
        print(
            f"Successfully bought {ticker.amount} shares of {ticker.symbol} at ${price:.2f} per share."
        )

    def sell_ticker(self, symbol: str, amount: float):
        """Sell a specific amount of a Ticker, adding proceeds to cash."""
        ticker = self.get_ticker(symbol)
        if not ticker:
            raise ValueError(f"Ticker {symbol} not in portfolio")
        if amount > ticker.amount:
            raise ValueError(
                f"Cannot sell {amount} shares; only {ticker.amount} available"
            )
            
        ticker.amount -= amount
        price = ticker.get_current_price()
        self.update_cash(amount * price)
        if ticker.amount == 0:
            self.tickers = [t for t in self.tickers if t.symbol != symbol]
            
        print(
            f"Successfully sold {ticker.amount} shares of {ticker.symbol} at ${price:.2f} per share."
        )

    def update_cash(self, amount: float):
        """Add or subtract from cash."""
        new_cash = self.cash + amount
        if new_cash < 0:
            raise ValueError("Cash cannot go negative")
        self.cash = new_cash

    def get_ticker(self, symbol: str) -> Ticker:
        """Retrieve a Ticker by its symbol."""
        return self.tickers.get(symbol)  # Returns None if symbol not found

    def calculate_total_value(self) -> float:
        """Calculate total portfolio value (cash + market value of tickers)."""
        total_ticker_value = 0.0
        for ticker in self.tickers.values():
            try:
                total_ticker_value += ticker.current_value()
            except Exception as e:
                print(f"Error fetching price for {ticker.symbol}: {e}")
                continue
        return self.cash + total_ticker_value

    def save_to_json(self):
        """Save portfolio to a JSON file."""
        data = {
            "cash": self.cash,
            "tickers": [
                {"symbol": symbol, "amount": ticker.amount}
                for symbol, ticker in self.tickers.items()
            ],
        }
        with open(self._file_path, "w") as f:
            json.dump(data, f, indent=4)
            
    def reset_portfolio(self):
        """Reset portfolio to default state and clear the JSON file."""
        self.cash = 0.0
        self.tickers = {}
        self.save_to_json()

    def __repr__(self):
        total_value = self.calculate_total_value()
        tickers_str = "\n".join(
            f"  - {symbol} - {ticker.amount} x ${ticker.get_current_price():.2f} = ${ticker.current_value():.2f}"
            for symbol, ticker in self.tickers.items()
        )
        return f"Portfolio total value: ${total_value:.2f}\n- Cash: ${self.cash:.2f}\n- Tickers:\n{tickers_str}"