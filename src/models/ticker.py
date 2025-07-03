"""
This module defines a Ticker class that represents a financial security.
"""

from dataclasses import dataclass 
from src.utils.yfinance_stock_data import get_ticker_price


@dataclass
class Ticker:
    """
    Represents a financial security held in a portfolio.

    Attributes:
        symbol (str): The stock ticker symbol (e.g., "MSFT").
        amount (float): The value or quantity held of the security.
    """

    symbol: str
    amount: float

    def get_current_price(self) -> float:
        """Fetch the current price of the stock using yfinance."""
        return get_ticker_price(self.symbol)

    def current_value(self) -> float:
        """Calculate the current total value of the holding."""
        return self.amount * self.get_current_price()
