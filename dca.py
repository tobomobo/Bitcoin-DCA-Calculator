from datetime import datetime, timedelta, timezone
import csv
from tabulate import tabulate
import yfinance as yf
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import argparse

class BitcoinDCA:
    def __init__(self, frequency, investment_amount, fee, duration):
        """
        Initializes the BitcoinDCA object with the given parameters and calculates the buy dates and historical prices.
        """
        self.frequency = frequency
        self.investment_amount = investment_amount
        self.fee = fee
        self.duration = duration
        self.buy_dates = self.calculate_buy_dates()
        self.historical_prices = self.request_historical_prices()

    def calculate_buy_dates(self):
        """
        Calculates the dates on which the user would buy Bitcoin based on the frequency and duration.
        Returns a list of datetime objects.
        """
        start_date = datetime.now(timezone.utc) - relativedelta(months=self.duration)
        end_date = datetime.now(timezone.utc)

        dates = []
        current_date = start_date

        if self.frequency == 'daily':
            delta = timedelta(days=1)
        elif self.frequency == 'weekly':
            delta = timedelta(days=7)
        else:  
            delta = relativedelta(months=1)

        while current_date <= end_date:
            dates.append(current_date)
            if self.frequency == 'monthly':
                current_date += relativedelta(months=1)
            else:
                current_date += delta

        return dates

    def request_historical_prices(self):
        """
        Requests historical Bitcoin prices for the calculated buy dates.
        Returns a dictionary mapping dates to prices.
        """
        start_date = min(self.buy_dates).strftime('%Y-%m-%d')
        end_date = max(self.buy_dates).strftime('%Y-%m-%d')

        btc = yf.download('BTC-USD', start=start_date, end=end_date)
        if btc.empty:
            return None

        historical_prices = btc['Close'].to_dict()
        historical_prices = {date.strftime('%Y-%m-%d'): price for date, price in historical_prices.items()}

        return historical_prices

    def calculate_satoshis(self, price, dca_amount, fees):
        """
        Calculates the number of satoshis (smallest unit of Bitcoin) that would be bought with the given amount and fees.
        Returns the number of satoshis.
        """
        fee_amount = dca_amount * (fees / 100)
        sats = (dca_amount - fee_amount) / price * 1e8
        return sats, fee_amount

    def write_csv(self):
        """
        Writes the calculated data to a CSV file.
        """
        with open('dca_purchases.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Buy Date', 'DCA Amount', 'Historical Price', 'Sats', 'Fee', 'Total Invested', 'Total Sats'])
            writer.writeheader()

            total_investment = 0
            total_sats = 0
            for d in self.buy_dates:
                date_str = d.strftime('%Y-%m-%d')
                if date_str in self.historical_prices:
                    buy_price = self.historical_prices[date_str]
                    sats, fee_amount = self.calculate_satoshis(buy_price, self.investment_amount, self.fee)
                    total_investment += self.investment_amount
                    total_sats += sats
                    purchase = {
                        'Buy Date': date_str,
                        'DCA Amount': self.investment_amount,
                        'Historical Price': buy_price,
                        'Sats': sats,
                        'Fee': fee_amount,
                        'Total Invested': total_investment,
                        'Total Sats': total_sats
                    }
                    writer.writerow(purchase)
                else:
                    print(f"Historical price not found for date {date_str}")

    def calculate_roi(self):
        """
        Calculates the return on investment based on the data in the CSV file.
        Returns the ROI as a float.
        """
        total_investment = 0
        total_sats = 0
        total_buys = 0
        total_fees = 0
        with open('dca_purchases.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_investment += float(row['DCA Amount'])
                total_sats += float(row['Sats'])
                total_buys += 1
                total_fees += float(row['Fee'])

        current_price = self.request_current_price()
        if current_price is not None:
            current_value = total_sats / 1e8 * current_price
            roi = ((current_value - total_investment) / total_investment) * 100
            return roi, total_fees
        else:
            print("Failed to retrieve current Bitcoin price.")
            return None, None

    def request_current_price(self):
        """
        Requests the current price of Bitcoin.
        Returns the current price as a float, or None if the request fails.
        """
        btc = yf.Ticker("BTC-USD")
        current_price = btc.history(period="1d")["Close"].iloc[-1]
        if current_price is not None:
            return current_price
        else:
            print("Failed to retrieve current Bitcoin price.")
            return None

    def plot_investment_vs_value(self):
        """
        Plots the nominal investment versus the current value of the investment.
        """
        invested_usd = []
        current_value = []
        dates = []
        total_investment = 0
        total_sats = 0
        total_buys = 0
        total_fees = 0

        with open('dca_purchases.csv', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                invested_usd.append(float(row['Total Invested']))
                current_value.append(float(row['Total Sats']) / 1e8 * float(row['Historical Price']))
                dates.append(datetime.strptime(row['Buy Date'], '%Y-%m-%d'))
                total_investment += float(row['DCA Amount'])
                total_sats += float(row['Sats'])
                total_buys += 1
                total_fees += float(row['Fee'])

        current_price = self.request_current_price()
        if current_price is not None:
            current_value_usd = total_sats / 1e8 * current_price
            roi, total_fees = self.calculate_roi()
            roi_str = f"ROI: {roi:.2f}%"
            total_investment_str = f"Nom. Investment: ${total_investment:.2f}"
<<<<<<< Updated upstream
            total_sats_str = f"Sats Purchased: {total_sats:.0f}"
            total_btc_str = f"BTC Purchased: {total_sats / 1e8:.8f}"
=======
            total_sats_str = f"Sats Purchased: {total_sats:.0f} sats"
            total_btc_str = f"BTC Purchased: {total_sats / 1e8:.8f} ₿"
>>>>>>> Stashed changes
            total_buys_str = f"Number of Purchases: {total_buys}"
            total_fees_str = f"Total Fees: ${total_fees:.2f}"
            current_value_str = f"Current Value: ${current_value_usd:.2f}"

            print(roi_str)
            print(total_buys_str)
            print(total_investment_str)
            print(total_sats_str)
            print(total_btc_str)
            print(total_fees_str)
            print(current_value_str)

            fig, ax = plt.subplots()
            ax.plot(dates, invested_usd, label='Invested USD')
            ax.plot(dates, current_value, label=f'Current Value ({roi_str})')

            date_formatter = mdates.DateFormatter('%Y-%m')
            ax.xaxis.set_major_formatter(date_formatter)
            fig.autofmt_xdate()

            plt.xlabel('Date')
            plt.ylabel('USD')
            plt.title('Nom. Investment vs Current Value')
            plt.legend(loc='upper left', labels=[f'Invested USD', f'Current Value ({roi_str})', f'Nom. Investment: {total_investment_str}', f'BTC Purchased: {total_sats_str}', f'Number of Purchases: {total_buys_str}', f'Total Fees: {total_fees_str}', f'Current Value: {current_value_str}'])
            plt.savefig('investment_vs_value.jpg', dpi=300, bbox_inches='tight')
            # plt.show()
        else:
            print("Failed to retrieve current Bitcoin price.")

    def print_csv_with_tabulate(self):
        """
        Prints the data in the CSV file in a tabulated format.
        """
        with open('dca_purchases.csv', 'r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(row for row in reader)
            if not rows:
                print("CSV file is empty.")
                return
            print(tabulate(rows, tablefmt="grid"))

def main():
    """
    The main function that parses command line arguments and runs the BitcoinDCA calculations.
    If any of the arguments are not provided or are invalid, it prompts the user for input until valid input is provided.
    It then creates a BitcoinDCA object, writes the data to a CSV file, prints the data in a tabulated format, and plots the investment versus value.
    """
    parser = argparse.ArgumentParser(description='Calculate the ROI of a Bitcoin DCA')
    parser.add_argument('-freq', '--frequency', choices=['daily', 'weekly', 'monthly'], default=None)
    parser.add_argument('-amount', '--investment_amount', type=float, default=None)
    parser.add_argument('-fee', '--fee', type=float, default=None)
    parser.add_argument('-duration', '--duration', type=int, default=None)
    args = parser.parse_args()

    frequency = args.frequency
    while frequency not in ['daily', 'weekly', 'monthly']:
        frequency = input("Please provide DCA frequency (Daily, Weekly, Monthly): ").lower()

    investment_amount = args.investment_amount
    while not isinstance(investment_amount, float) or investment_amount <= 0:
        try:
            investment_amount = float(input("Please provide DCA amount (positive number): "))
        except ValueError:
            print("Invalid input. Please enter a positive number.")

    fee = args.fee
    while not isinstance(fee, float) or fee <= 0:
        try:
            fee = float(input("Exchange Fees in % (Format: 1% or 0.5%) excluding the % sign: "))
        except ValueError:
            print("Invalid input. Please enter a positive number.")

    duration = args.duration
    while not isinstance(duration, int) or duration <= 0:
        try:
            duration = int(input("Please provide DCA Duration in months (positive number): "))
        except ValueError:
            print("Invalid input. Please enter a positive number.")

    dca = BitcoinDCA(frequency, investment_amount, fee, duration)
    dca.write_csv()
    dca.print_csv_with_tabulate()
    dca.plot_investment_vs_value()

if __name__ == "__main__":
    main()