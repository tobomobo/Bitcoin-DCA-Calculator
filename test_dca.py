import os
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import sys
from dca import BitcoinDCA, main
import sys

import matplotlib.pyplot as plt

def test_bitcoin_dca_init():
    # Test the initialization of BitcoinDCA class
    dca = BitcoinDCA('daily', 100, 0.5, 6)
    assert dca.frequency == 'daily'
    assert dca.investment_amount == 100
    assert dca.fee == 0.5
    assert dca.duration == 6

def test_calculate_buy_dates():
    # Test the calculation of buy dates
    dca = BitcoinDCA('daily', 100, 0.5, 6)
    buy_dates = dca.calculate_buy_dates()
    assert len(buy_dates) > 0
    assert all(date <= datetime.now(timezone.utc) for date in buy_dates)

def test_request_historical_prices():
    # Test the request for historical prices
    dca = BitcoinDCA('daily', 100, 0.5, 6)
    historical_prices = dca.request_historical_prices()
    assert isinstance(historical_prices, dict)
    assert all(isinstance(date, str) and isinstance(price, (int, float)) for date, price in historical_prices.items())

def test_calculate_satoshis():
    # Test the calculation of satoshis and fee amount
    dca = BitcoinDCA('daily', 100, 0.5, 6)
    satoshis, fee_amount = dca.calculate_satoshis(40000, 100, 0.5)
    assert isinstance(satoshis, (int, float))
    assert isinstance(fee_amount, (int, float))

def test_write_csv():
    # Test the writing of CSV file
    dca = BitcoinDCA('daily', 100, 0.5, 6)
    dca.write_csv()
    assert 'dca_purchases.csv' in os.listdir()

def test_calculate_roi():
    # Test the calculation of ROI and total fees
    dca = BitcoinDCA('daily', 100, 0.5, 6)
    roi, total_fees = dca.calculate_roi()
    assert isinstance(roi, (int, float))
    assert isinstance(total_fees, (int, float))

def test_plot_investment_vs_value():
    # Test the plotting of investment vs value
    dca = BitcoinDCA('daily', 100, 0.5, 6)
    dca.plot_investment_vs_value()
    assert 'investment_vs_value.jpg' in os.listdir()

def test_print_csv_with_tabulate():
    # Test the printing of CSV file using tabulate
    dca = BitcoinDCA('daily', 100, 0.5, 6)
    dca.print_csv_with_tabulate()
    pass

def test_main():
    # Test the main function
    sys.argv = ['dca.py', '-freq', 'daily', '-amount', '100', '-fee', '0.5', '-duration', '6']
    main()
    assert True