import os
import csv
import matplotlib.pyplot as plt
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import sys
from dca import main, calculate_buy_dates, request_historical_prices, calculate_satoshis, write_csv, calculate_roi, request_current_price, plot_investment_vs_value, print_csv_with_tabulate

# Test the main function
def test_main(capsys):
    # Set command line arguments
    sys.argv = ['dca.py', '-freq', 'monthly', '-amount', '1000', '-fee', '1', '-duration', '36']
    # Run the main function
    main()
    # Capture the output
    captured = capsys.readouterr()
    # Assert that the output contains the expected strings
    assert 'ROI: ' in captured.out
    assert 'Number of Purchases: 36' in captured.out
    assert 'Nom. Investment: $36000.00' in captured.out
    assert 'BTC Purchased: ' in captured.out
    assert 'Current Value: ' in captured.out

# Test the calculate_buy_dates function
def test_calculate_buy_dates():
    # Calculate buy dates for daily frequency and 1 month duration
    dates = calculate_buy_dates('daily', 1)
    # Assert that the dates list is not empty and the first date is a datetime object
    assert len(dates) > 0
    assert isinstance(dates[0], datetime)

# Test the request_historical_prices function
def test_request_historical_prices():
    # Create a list of dates
    dates = [datetime.now(timezone.utc) - relativedelta(days=1), datetime.now(timezone.utc)]
    # Request historical prices for the dates
    prices = request_historical_prices(dates)
    # Assert that the prices are not None and are a dictionary
    assert prices is not None
    assert isinstance(prices, dict)

# Test the calculate_satoshis function
def test_calculate_satoshis():
    # Calculate satoshis for a price of 40000, DCA amount of 100, and fee of 1
    satoshis, fee_amount = calculate_satoshis(40000, 100, 1)
    # Assert that the satoshis and fee amount are greater than 0
    assert satoshis > 0
    assert fee_amount > 0

# Test the write_csv function
def test_write_csv(tmp_path):
    # Create a list of dates
    dates = [datetime.now(timezone.utc) - relativedelta(days=1), datetime.now(timezone.utc)]
    # Create a dictionary of prices
    prices = {date.strftime('%Y-%m-%d'): 40000 for date in dates}
    # Write the DCA purchases to a CSV file
    write_csv(dates, 100, 1, prices)
    # Assert that the CSV file exists
    assert os.path.exists('dca_purchases.csv')

# Test the calculate_roi function
def test_calculate_roi():
    # Calculate the ROI
    roi = calculate_roi()
    # Assert that the ROI is not None and is a number
    assert roi is not None
    assert isinstance(roi, (int, float))

# Test the request_current_price function
def test_request_current_price():
    # Request the current Bitcoin price
    price = request_current_price()
    # Assert that the price is not None and is a number
    assert price is not None
    assert isinstance(price, (int, float))

# Test the plot_investment_vs_value function
def test_plot_investment_vs_value(monkeypatch):
    # Monkeypatch the plt.show function to do nothing
    monkeypatch.setattr(plt, 'show', lambda: None)
    # Plot the investment vs value
    plot_investment_vs_value()

# Test the print_csv_with_tabulate function
def test_print_csv_with_tabulate():
    # Create a CSV file with a header and a row
    with open('dca_purchases.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Buy Date', 'DCA Amount', 'Historical Price', 'Sats', 'Fee', 'Total Invested', 'Total Sats'])
        writer.writeheader()
        writer.writerow({'Buy Date': '2022-01-01', 'DCA Amount': 100, 'Historical Price': 40000, 'Sats': 100000, 'Fee': 1, 'Total Invested': 100, 'Total Sats': 100000})
    # Print the CSV file with tabulate
    print_csv_with_tabulate()