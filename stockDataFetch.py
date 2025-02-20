# Importing libraries

# yahoo finance library for fetching the financial data from yahoo finance
import yfinance as yf

# os library for saving the file
import os

# for adding delay so that during the download process of the stocks data for many stocks, it don't get clashed
# and the downloading part takes place smoothly.
import time


# Function
def fetch_stock_data():
    # Stock names of 50 Stocks
    stock_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX", "ADBE", "AMD",
                     "INTC", "CSCO", "IBM", "ORCL", "PYPL", "QCOM", "UBER", "BABA", "V", "MA",
                     "JPM", "BAC", "GS", "C", "WFC", "PEP", "KO", "PG", "UNH", "JNJ",
                     "PFE", "MRNA", "LLY", "ABT", "T", "VZ", "DIS", "NKE", "MCD", "SBUX",
                     "BA", "GE", "CAT", "MMM", "DE", "HON", "XOM", "CVX", "BP", "SHEL"]

    # Name and directory of the folder where all the files will be saved
    folder_name = "StockData_1H-1Y"
    os.makedirs(folder_name, exist_ok=True)

    # Setting values for interval and period
    interval = "1h"  # 1h not 4h because yahoo finance api doesn't provide interval of 4H. 1H was closest to 4H so.....
    period = "1y"

    # Main data collection logic and loop.
    for symbol in stock_symbols:
        print(f"Fetching data for the stock: {symbol}")
        try:
            # Creating a Ticker object
            stock = yf.Ticker(symbol)

            # Fetching the historical data for each stock
            df = stock.history(interval=interval, period=period)

            # Saving file after downloading data to given path with given name
            filePath = os.path.join(folder_name, f"{symbol}_1H-1Y.csv")
            df.to_csv(filePath)

            # Printing Confirming Statement for Surety!
            print(f"Data saved for the Stock: {symbol} in {filePath}\n")

            # Adding delay of 2 sec
            time.sleep(2)

        # Handling exception
        except Exception as e:
            print(f"Error Retrieving data of the stock: {symbol}.\nError is : {e}\n")
