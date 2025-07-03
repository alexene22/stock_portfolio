""" "
This module defines a Portfolio class that represents a stock portfolio.
"""
from pathlib import Path
import json

from src.models.ticker import Ticker

class Portfolio:
    """
    A class to represent a stock portfolio.

    Attributes:
        cash (float): The amount of cash available in the portfolio
        tickers (dict): A dictionary mapping ticker symbols to Ticker objects        
        file_path: Path to the JSON file for saving/loading portfolio data
    """
    def __init__(self):
        """Initialize portfolio from JSON file or use default values."""
        self.tickers = {}
        self.cash = 0.0
        self.file_path = None
        
        # Portfolio file path setup
        project_root = Path(__file__).resolve().parents[2]
        self.file_path = project_root / "data" / "portfolio.json"
        
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
            
            self.cash = data.get("cash")    
            self.tickers = {
                item["symbol"]: Ticker(symbol=item["symbol"], amount=item["amount"])
                for item in data.get("tickers")
            }            
        except FileNotFoundError:
            print(f"Portfolio file {self.file_path} not found. Using default portfolio.")
        except json.JSONDecodeError as e:
            print(f"Error reading JSON file: {e}. Using default portfolio.")


    def buy_ticker(self, ticker: Ticker):
        """Add or update a Ticker object in the portfolio, deducting cost from cash."""
        if ticker.amount <= 0:
            raise ValueError("Ticker amount cannot be negative or zero")
        
        price = ticker.get_current_price()
        cost = ticker.amount * price
        if cost > self.cash:
            raise ValueError(f"Insufficient cash: need ${cost:.2f}, available ${self.cash:.2f}")
            
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

    def sell_ticker(self, ticker:Ticker):
        """Sell a specific amount of a Ticker, adding proceeds to cash."""
        portfolio_ticker = self.get_ticker(ticker.symbol)
        if not portfolio_ticker:
            raise ValueError(f"Ticker {ticker.symbol} not in portfolio")
        
        if ticker.amount <= 0:
            raise ValueError("Ticker amount must be positive")
        elif ticker.amount > portfolio_ticker.amount:
            raise ValueError(f"Cannot sell {ticker.amount} shares; only {portfolio_ticker.amount} available")
            
        portfolio_ticker.amount -= ticker.amount
        price = portfolio_ticker.get_current_price()
        self.update_cash(ticker.amount * price)
        if portfolio_ticker.amount == 0:
            del self.tickers[ticker.symbol]
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
        with open(self.file_path, "w") as f:
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