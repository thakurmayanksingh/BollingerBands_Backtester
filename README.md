# BollingerBands_Backtester
 BollingerBands_Backtester is an interactive Python project that uses data-driven insights with visualization. It collects historical stock data (using 1-hour candles for the last year) through the yfinance API, uses Bollinger Bands to detect volatility, and subsequently simulates a trading strategy: it buys when prices fall 3% below the lower band and sells when they touch or go above the upper band. The results are stored to a CSV file for keeping records, and a simple web application allows you to analyze the trade performance with easy-to-understand charts.

# How to Run the Scripts:
(1) Run main.py first. This script fetches stock data and executes the backtesting process.
(2) Choose one of the two available visualization options to view your results.

Thank you,
Mayank
