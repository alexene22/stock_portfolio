# 📈 Stock Portfolio Manager

A simple command-line application to simulate buying, selling, and managing stock tickers in a virtual portfolio using real-time market data via Yahoo Finance.

## 🚀 Features

- 💼 Manage a virtual portfolio
- 📊 Buy and sell stock tickers using live prices  
- 💸 Add cash to your portfolio  
- 🗃️ Automatically persists data to JSON  
- 🧪 Reset portfolio to default state  
- 🧠 Real-time price data via `yfinance`

## 🧱 Project Structure

```
stock_portfolio/
├── docs/               # Sphinx documentation
├── src/                # Source code
│   ├── main.py         # Main script
│   ├── models/
│   │   ├── ticker.py       # Ticker class
│   │   └── portfolio.py    # Portfolio class
│   └── utils/
│       └── yfinance_stock_data.py  # Pulls data via yfinance
```

## 🛠️ Installation

```bash
git clone https://github.com/alexene22/stock_portfolio
cd stock_portfolio
pip install -r requirements.txt
```

**Requirements**:

```
yfinance
```

## ▶️ Running the App

From the root of the project:

```bash
python -m src.main
```

## 🧑‍💻 Example Interaction

```
=== Stock Portfolio Manager ===
0. View Portfolio
1. Buy Ticker
2. Sell Ticker
9. Add Cash
R. Reset Portfolio
X. Exit
==========================
Enter your choice: 9
Enter amount of cash to add: 10000
Successfully added $10000.00 to portfolio cash.

==========================
Enter your choice: 1
Enter ticker symbol: MSFT
Enter number of shares to buy: 10
Successfully bought 10 shares of MSFT.

==========================
Enter your choice: 1
Enter ticker symbol: AAPL
Enter number of shares to buy: 5
Successfully bought 5 shares of AAPL.

==========================
Enter your choice: 0

PORTFOLIO SUMMARY:
- Cash Balance: $9,500.00
- Total Value: $10,250.00 (est.)
  
HOLDINGS:
1. MSFT: 10 shares ($750.00 est.)
2. AAPL: 5 shares ($500.00 est.)

==========================
Enter your choice: 2
Enter ticker symbol to sell: AAPL
Enter number of shares to sell (max 5): 3
Successfully sold 3 shares of AAPL.

==========================
Enter your choice: 0

PORTFOLIO SUMMARY:
- Cash Balance: $9,800.00
- Total Value: $10,550.00 (est.)
  
HOLDINGS:
1. MSFT: 10 shares ($750.00 est.)
2. AAPL: 2 shares ($200.00 est.)
```

## 📚 Building Documentation

To build the Sphinx documentation:

```bash
cd docs
sphinx-apidoc -o . ../src
make html
```

Open the documentation in your browser:

```
docs/_build/html/index.html
```

## 🧾 TODO

- Manage portfolio performance over time  
- Add graphs and charts  
- Optional GUI/streamlit interface  

## 📄 License

MIT License
