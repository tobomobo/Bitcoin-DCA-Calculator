from datetime import datetime, timedelta, timezone
import csv
from tabulate import tabulate
import yfinance as yf
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Calculate the ROI of a Bitcoin DCA')
    parser.add_argument('-freq', '--frequency', choices=['daily', 'weekly', 'monthly'], default=None)
    parser.add_argument('-amount', '--investment_amount', type=float, default=None)
    parser.add_argument('-fee', '--fee', type=float, default=None)
    parser.add_argument('-duration', '--duration', type=int, default=None)
    args = parser.parse_args()

    # Get user input for frequency, investment amount, fee, and duration if not provided as arguments
    frequency = args.frequency
    investment_amount = args.investment_amount
    fee = args.fee
    duration = args.duration

    if frequency is None:
        frequency = input("Please provide DCA frequency (Daily, Weekly, Monthly): ")
    if investment_amount is None:
        investment_amount = float(input("Please provide DCA amount (positive number): "))
    if fee is None:
        fee = float(input("Exchange Fees in % (Format: 1% or 0.5%) excluding the % sign: "))
    if duration is None:
        duration = int(input("Please provide DCA Duration in months (positive number): "))

    # Calculate buy dates based on frequency and duration
    buy_dates = calculate_buy_dates(frequency, duration)
    historical_prices = request_historical_prices(buy_dates)

    if historical_prices is not None:
        # Write DCA purchases to CSV file
        write_csv(buy_dates, investment_amount, fee, historical_prices)
        # Print CSV file with tabulate
        print_csv_with_tabulate()
        # Calculate ROI
        calculate_roi()
        # Plot investment vs value
        plot_investment_vs_value()
    else:
        print("Failed to retrieve historical prices.")

def get_valid_input(prompt, conversion_function, condition, error_message):
    # Get valid user input
    while True:
        try:
            input_value = conversion_function(input(prompt).strip())
            if not condition(input_value):
                raise ValueError
            return input_value
        except ValueError:
            print(error_message)

def calculate_buy_dates(frequency, duration):
    # Calculate buy dates based on frequency and duration
    start_date = datetime.now(timezone.utc) - relativedelta(months=duration)
    end_date = datetime.now(timezone.utc)

    dates = []
    current_date = start_date

    if frequency == 'daily':
        delta = timedelta(days=1)
    elif frequency == 'weekly':
        delta = timedelta(days=7)
    else:  # monthly
        delta = relativedelta(months=1)

    while current_date <= end_date:
        dates.append(current_date)
        if frequency == 'monthly':
            current_date += relativedelta(months=1)
        else:
            current_date += delta

    return dates

def request_historical_prices(buy_dates):
    # Request historical prices from Yahoo Finance
    start_date = min(buy_dates).strftime('%Y-%m-%d')
    end_date = max(buy_dates).strftime('%Y-%m-%d')

    btc = yf.download('BTC-USD', start=start_date, end=end_date)
    if btc.empty:
        return None

    historical_prices = btc['Close'].to_dict()
    historical_prices = {date.strftime('%Y-%m-%d'): price for date, price in historical_prices.items()}

    return historical_prices

def calculate_satoshis(price, dca_amount, fees):
    # Calculate satoshis purchased
    fee_amount = dca_amount * (fees / 100)
    sats = (dca_amount - fee_amount) / price * 1e8
    return sats, fee_amount

def write_csv(buy_dates, dca_amount, fees, historical_prices):
    # Write DCA purchases to CSV file
    with open('dca_purchases.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Buy Date', 'DCA Amount', 'Historical Price', 'Sats', 'Fee', 'Total Invested', 'Total Sats'])
        writer.writeheader()

        total_investment = 0
        total_sats = 0
        for d in buy_dates:
            date_str = d.strftime('%Y-%m-%d')
            if date_str in historical_prices:
                buy_price = historical_prices[date_str]
                sats, fee_amount = calculate_satoshis(buy_price, dca_amount, fees)
                total_investment += dca_amount
                total_sats += sats
                purchase = {
                    'Buy Date': date_str,
                    'DCA Amount': dca_amount,
                    'Historical Price': buy_price,
                    'Sats': sats,
                    'Fee': fee_amount,
                    'Total Invested': total_investment,
                    'Total Sats': total_sats
                }
                writer.writerow(purchase)
            else:
                print(f"Historical price not found for date {date_str}")

def calculate_roi():
    # Calculate ROI
    total_investment = 0
    total_sats = 0
    total_buys = 0
    with open('dca_purchases.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_investment += float(row['DCA Amount'])
            total_sats += float(row['Sats'])
            total_buys += 1

    current_price = request_current_price()
    if current_price is not None:
        current_value = total_sats / 1e8 * current_price
        roi = ((current_value - total_investment) / total_investment) * 100
        return roi
    else:
        print("Failed to retrieve current Bitcoin price.")
        return None

def request_current_price():
    # Request current Bitcoin price from Yahoo Finance
    btc = yf.Ticker("BTC-USD")
    current_price = btc.history(period="1d")["Close"].iloc[-1]
    if current_price is not None:
        return current_price
    else:
        print("Failed to retrieve current Bitcoin price.")
        return None

def plot_investment_vs_value():
    # Plot investment vs value
    invested_usd = []
    current_value = []
    dates = []
    total_investment = 0
    total_sats = 0
    total_buys = 0

    with open('dca_purchases.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            invested_usd.append(float(row['Total Invested']))
            current_value.append(float(row['Total Sats']) / 1e8 * float(row['Historical Price']))
            dates.append(datetime.strptime(row['Buy Date'], '%Y-%m-%d'))
            total_investment += float(row['DCA Amount'])
            total_sats += float(row['Sats'])
            total_buys += 1

    current_price = request_current_price()
    if current_price is not None:
        current_value_usd = total_sats / 1e8 * current_price
        roi = calculate_roi()
        roi_str = f"ROI: {roi:.2f}%"
        total_investment_str = f"Nom. Investment: ${total_investment:.2f}"
        total_sats_str = f"Sats Purchased: {total_sats:.0f}"
        total_btc_str = f"BTC Purchased: {total_sats / 1e8:.8f}"
        total_buys_str = f"Number of Purchases: {total_buys}"
        current_value_str = f"Current Value: ${current_value_usd:.2f}"

        print(roi_str)
        print(total_buys_str)
        print(total_investment_str)
        print(total_sats_str)
        print(total_btc_str)
        print(current_value_str)

        fig, ax = plt.subplots()
        ax.plot(dates, invested_usd, label='Invested USD')
        ax.plot(dates, current_value, label=f'Current Value ({roi_str})')

        # Format the dates
        date_formatter = mdates.DateFormatter('%Y-%m')
        ax.xaxis.set_major_formatter(date_formatter)
        fig.autofmt_xdate()

        plt.xlabel('Date')
        plt.ylabel('USD')
        plt.title('Nom. Investment vs Current Value')
        plt.legend(loc='upper left', labels=[f'Invested USD', f'Current Value ({roi_str})', f'Nom. Investment: {total_investment_str}', f'BTC Purchased: {total_sats_str}', f'Number of Purchases: {total_buys_str}', f'Current Value: {current_value_str}'])
        plt.savefig('investment_vs_value.jpg', dpi=300, bbox_inches='tight')
        # plt.show()
    else:
        print("Failed to retrieve current Bitcoin price.")

def print_csv_with_tabulate():
    # Print CSV file with tabulate
    with open('dca_purchases.csv', 'r', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(row for row in reader)
        if not rows:
            print("CSV file is empty.")
            return
        print(tabulate(rows, tablefmt="grid"))

if __name__ == "__main__":
    main()
