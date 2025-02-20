# Importing libraries
import pandas as pd
import os


# Function for Calculation of Bollinger Bands. This method returns modified dataframe with following columns:
# (SMA, STD, Upper_Band, Lower_Band)
def calculate_bollinger_bands(df, window=20, std_dev=2):
    # Calculating SMA (Simple Moving Average): Computing the average of the last n closing prices
    df['SMA'] = df['Close'].rolling(window).mean()

    # Calculating STD (Rolling Standard Deviation). Measures the volatility (spread) of the stocks of n prices
    df['STD'] = df['Close'].rolling(window).std()

    # Calculating Upper_Band. (Upper Band = df[sma] + (std_dev * df[std]))
    df['Upper_Band'] = (df['SMA'] + (std_dev * df['STD']))

    # Calculating Lower_Band. (Lower Band = df[sma] - (std_dev * df[std]))
    df['Lower_Band'] = (df['SMA'] - (std_dev * df['STD']))

    # Dropping NaN Values
    df.dropna()

    # Returning a dataframe with columns : (SMA, STD, Upper_Band, Lower_Band)
    return df


# Creating Bollinger Back Test class
class BollingerBacktest:
    # Initialize function for the class
    def __init__(self, data_folder, output_file):
        self.data_folder = data_folder
        self.output_file = output_file
        self.trades = []

    # Function for running the backtest logic. This code performs three tasks i.e.
    # (1) Loops through all csv files in the data_folder
    # (2) Applies the bollinger calculation bands
    # (3) Atlast, run the backtest on each stock (token)
    def run_backtest(self):
        # Iterating through each file in the data_folder whose extension is .csv
        for file in os.listdir(self.data_folder):
            if file.endswith(".csv"):

                # Extracting stock symbol/token from the file name
                token = file.split("_")[0]
                print(f"Processing {token}...")

                # reading the data of the file
                data = pd.read_csv(os.path.join(self.data_folder, file), index_col=0, parse_dates=True)

                # data check i.e. skips the file if it doesn't contain 'Close' or if df is empty
                if data.empty or 'Close' not in data.columns:
                    print("Skipping {token} due to missing data...")
                    continue

                # Bollinger Bands Calculation
                data = calculate_bollinger_bands(data)

                # Backtesting per token
                self.backtest_token(token, data)

                # saving results
                self.save_results()

    # Simulating trade strategy for a given stock (token) using bollinger bands with this backtest_token function
    def backtest_token(self, token, data):
        # Initial Variables
        position = 0  # For tracking whether trade is active or not
        buy_price = None  # records price when position is opened
        date_in = None  # records date when position is opened

        # Looping over the data
        for i in range(len(data)):
            close = data.iloc[i]['Close']
            lower_band = data.iloc[i]['Lower_Band']
            upper_band = data.iloc[i]['Upper_Band']
            date = data.index[i]

            # TRADING LOGIC STARTS

            # Buy Logic - Buy a stock if price is 3% less than the lower bollinger band and there is no open position
            if close < (lower_band * 0.97) and position == 0:
                # Action to take is buying the stocks worth $100, setting buy_price and date_in and printing a message
                position = 100/close
                buy_price = close
                date_in = date
                print(f"\nBUY {token}: Bought at {buy_price} on {date_in}")

            # Sell Logic - Selling a stock if it's price touches or exceeds the upper bollinger band and no open pos
            elif close >= upper_band and position == 0:
                sell_price = close
                if buy_price is None or sell_price is None:
                    continue
                profit_percentage = ((sell_price - buy_price) / buy_price) * 100
                self.trades.append([token, date_in, buy_price, date, sell_price, profit_percentage])
                position = 0
                print(f"\nSELL {token}: Sold at {sell_price} on {date}, Profit: {profit_percentage:.2f}%\n")

        # Final Check if there is any position still left open then close it
        if position > 0:
            sell_price = data.iloc[-1]['Close']
            if buy_price is None or sell_price is None:
                pass
            else:
                profit_percentage = ((sell_price - buy_price) / buy_price) * 100
                self.trades.append([token, date_in, buy_price, data.index[-1], sell_price, profit_percentage])
                print(f"\nEXIT {token}: Sold at {sell_price} on {data.index[-1]}, Final Profit: {profit_percentage:.2f}%")

    # Function for saving the results into a resultant file.
    def save_results(self):
        # Creating a dataframe object
        df = pd.DataFrame(self.trades,
                          columns=['token', 'date_in', 'buy_price', 'date_out', 'sell_price', 'profit_percentage'])

        # Converting it to a csv file and then printing
        df.to_csv(self.output_file, index=False)
        print(f"Results saved to {self.output_file}")

        # Printing those stocks which are left because there buy-sell condition don't get triggered...
        processed_tokens = set(df['token'].unique())
        original_stock_list = {
            "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "AMD",
            "INTC", "CSCO", "IBM", "ORCL", "PYPL", "QCOM", "UBER", "BABA", "V", "MA",
            "JPM", "BAC", "GS", "C", "WFC", "PEP", "KO", "PG", "UNH", "JNJ",
            "PFE", "MRNA", "LLY", "ABT", "T", "VZ", "DIS", "NKE", "MCD", "SBUX",
            "BA", "GE", "CAT", "MMM", "DE", "HON", "XOM", "CVX", "BP", "SHEL"
        }
        missing_tokens = original_stock_list - processed_tokens
        print(
            f'\nMissing Stocks:\n{missing_tokens}\nThese stocks are missing because they did\'nt trigger buy '
            f'conditions.')


if __name__ == '__main__':
    data_folder = "StockData_1H-1Y"
    output_file = "backtest_results.csv"
    backtest = BollingerBacktest(data_folder, output_file)
    backtest.run_backtest()