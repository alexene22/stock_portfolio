"""MAIN MODULE FOR STOCK PORTFOLIO MANAGER"""

import os
import sys
sys.path.append((os.path.dirname(os.getcwd())))

from src.models.ticker import Ticker
from src.models.portfolio import Portfolio


def display_menu():
    """Display the main menu for the Stock Portfolio Manager."""
    print("\n=== Stock Portfolio Manager ===")
    print("0. View Portfolio")
    print("1. Buy Ticker")
    print("2. Sell Ticker")
    print("9. Add Cash")
    print("R. Reset Portfolio")
    print("X. Exit")
    print("==========================")


def get_float_input(prompt: str) -> float:
    """Prompt for a float input with validation."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def get_symbol_input(prompt: str) -> str:
    """Prompt for a ticker symbol input with validation."""
    while True:
        symbol = input(prompt).strip().upper()
        if symbol and symbol.isalnum():
            return symbol
        print("Please enter a valid ticker symbol (alphanumeric).")


def main():
    """Main function to run the Stock Portfolio Manager."""
    portfolio = Portfolio()  # Initialize portfolio with 10000 cash

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip().upper()

        if choice == "0":  # View Portfolio
            print(portfolio)

        elif choice == "1":  # Buy Ticker
            symbol = get_symbol_input("Enter ticker symbol: ")
            amount = get_float_input("Enter number of shares to buy: ")
            
            try:
                portfolio.buy_ticker(Ticker(symbol=symbol, amount=amount))
                portfolio.save_to_json()
            except ValueError as e:
                print(f"Error: {e}")            

        elif choice == "2":  # Sell Ticker
            symbol = get_symbol_input("Enter ticker symbol to sell: ")
            
            ticker = portfolio.get_ticker(symbol)            
            if not ticker:
                print(f"Error: {symbol} not found in portfolio.")
                continue
            
            amount = get_float_input(f"Enter number of shares to sell (max {ticker.amount}): ")
            if amount > ticker.amount:
                print(f"Error: Cannot sell {amount} shares; only {ticker.amount} available.")
                continue

            try:
                portfolio.sell_ticker(Ticker(symbol=symbol, amount=amount))
                portfolio.save_to_json()                
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "9":  # Add Cash
            amount = get_float_input("Enter amount of cash to add: ")
            
            try:
                portfolio.update_cash(amount)
                portfolio.save_to_json()
                print(f"Successfully added ${amount:.2f} to portfolio cash.")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "R":  # Reset Portfolio
            confirm = input("Are you sure you want to reset the portfolio? (Y/N): ").strip().upper()
            if confirm == "Y":
                portfolio.reset_portfolio()
                print("Portfolio has been reset to default state.")
            else:
                print("Portfolio reset cancelled.")
        
        elif choice == "X":  # Exit
            confirm = input("Are you sure you want to exit? (Y/N): ").strip().upper()
            if confirm == "Y":
                print("Exiting Portfolio Manager. Goodbye!")
                break
            else:
                print("Exit cancelled. Returning to main menu.")

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
