# Importing Libraries
import time
from stockDataFetch import fetch_stock_data
from backtestingCode import BollingerBacktest

# Defining paths
DATA_FOLDER = "StockData_1H-1Y"
OUTPUT_FILE = "backtest_results.csv"


# Main method
def main():
    # Fetching the Stock Data
    print("Starting stock data download...\n")
    fetch_stock_data()
    print("Stock data download completed.\n")

    # Implementing the Backtest Part
    print("Starting Bollinger Band Backtest...\n")
    backtest = BollingerBacktest(DATA_FOLDER, OUTPUT_FILE)
    backtest.run_backtest()
    print("\nBacktesting completed. Check results in:", OUTPUT_FILE)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"\nTotal Execution Time: {time.time() - start_time:.2f} seconds")
