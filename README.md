# Bitcoin DCA ROI Calculator
=====================

#### Video Demo:

#### Description:
-----
This is a command-line tool to calculate the ROI of a Bitcoin Dollar Cost Averaging (DCA) strategy. It uses historical Bitcoin prices from Yahoo Finance to simulate the investment and calculate the return on investment (ROI).

### Usage
-----

To use this tool, simply run the `dca.py` script with the following optional arguments:

* `-freq` or `--frequency`: The frequency of the DCA strategy (daily, weekly, or monthly). Default is to prompt the user for input.
* `-amount` or `--investment_amount`: The amount of money to invest each period. Default is to prompt the user for input.
* `-fee` or `--fee`: The exchange fee as a percentage (e.g. 1% or 0.5%). Default is to prompt the user for input.
* `-duration` or `--duration`: The duration of the DCA strategy in months. Default is to prompt the user for input.

### Example
-----

```
$ python dca.py -freq weekly -amount 100 -fee 0.5 -duration 6
```

### Output
-----

The tool will generate a CSV file `dca_purchases.csv` containing the simulated investment data. It will also print the ROI and other statistics to the console. Additionally, it will generate a plot of the investment vs. current value over time and save it as `investment_vs_value.jpg`.

### Requirements
------------

* Python 3.8+
* `yfinance` library for historical price data
* `tabulate` library for pretty-printing the CSV data
* `matplotlib` library for plotting

```
$ pip install -r requirements.txt
```