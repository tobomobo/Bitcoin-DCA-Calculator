# Bitcoin DCA ROI Calculator

## Description: 
This is a command-line tool to calculate the ROI of a Bitcoin Dollar Cost Averaging (DCA) strategy. It uses historical Bitcoin prices from Yahoo Finance to simulate the investment and calculate the return on investment (ROI).

## **What is Bitcoin?**

Bitcoin is a decentralized digital currency that allows for peer-to-peer transactions without the need for intermediaries like banks. It's a store of value, a medium of exchange, and a unit of account. Bitcoin is not controlled by any government or institution, and its supply is capped at 21 million, making it a scarce asset. This scarcity, combined with its limited supply, makes it a valuable store of value.

## **Why is a Bitcoin DCA necessary?**

In today's fiat currency system, central banks have the power to print money at will, which leads to inflation and devaluation of currencies. This devaluation erodes the purchasing power of money, making it difficult for individuals to save and invest. Bitcoin, on the other hand, is a decentralized and limited supply asset that is not subject to the whims of central banks. By investing in Bitcoin, individuals can protect their purchasing power and increase their wealth over time.

## **What is a Bitcoin DCA?**

A Bitcoin DCA is a strategy that involves investing a fixed amount of money in Bitcoin at regular intervals, regardless of the market price. This strategy helps to reduce the impact of market volatility and timing risks, as it eliminates the need to predict the market's direction. By investing regularly, individuals can take advantage of the power of compounding and potentially increase their returns over time.

### Usage

---

To use this tool, simply run the `dca.py` script with the following optional arguments:

- `-freq` or `--frequency`: The frequency of the DCA strategy (daily, weekly, or monthly). Default is to prompt the user for input.
- `-amount` or `--investment_amount`: The amount of money to invest each period. Default is to prompt the user for input.
- `-fee` or `--fee`: The exchange fee as a percentage (e.g. 1% or 0.5%). Default is to prompt the user for input.
- `-duration` or `--duration`: The duration of the DCA strategy in months. Default is to prompt the user for input.

### Example

---

```
$ python dca.py -freq weekly -amount 500 -fee 0.79 -duration 24
```

### Output

---

The tool will generate a CSV file `dca_purchases.csv` containing the simulated investment data. It will also print the ROI and other statistics to the console. Additionally, it will generate a plot of the investment vs. current value over time and save it as `investment_vs_value.jpg`.

### Requirements

---

- Python 3.8+
- `yfinance` library for historical price data
- `tabulate` library for pretty-printing the CSV data
- `matplotlib` library for plotting

```
$ pip install -r requirements.txt
```

### Disclaimer
This tool is for educational purposes only and is not intended to be taken as financial advice. However, any rational person should read a book or two about Bitcoin to understand the basics of sound money and the dangers of fiat currency.