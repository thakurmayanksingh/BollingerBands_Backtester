# Importing libraries
from flask import Flask, render_template, request
import pandas as pd
import os
import plotly.graph_objects as go
from backtestingCode import calculate_bollinger_bands

# Creating an object
app = Flask(__name__, template_folder="templates_v1")

# Defining paths of the directories
DATA_FOLDER = "StockData_1H-1Y"
RESULTS_FILE = "backtest_results.csv"


# Loading available stocks
def get_stock_list():
    return [f.split("_")[0] for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]


# Loading stock data
def load_stock_data(stock):
    file_path = os.path.join(DATA_FOLDER, f"{stock}_1H-1Y.csv")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    # Ensuring that Bollinger Bands are being calculated
    if "SMA" not in df.columns:
        df = calculate_bollinger_bands(df)

    # returning the dataframe - df
    return df


# Loading backtest results
def load_backtest_results():
    df = pd.read_csv(RESULTS_FILE)
    return df


@app.route("/")
def index():
    stocks = get_stock_list()
    return render_template("index.html", stocks=stocks)


@app.route("/visualize", methods=["POST"])
def visualize():
    stock = request.form.get("stock")
    df = load_stock_data(stock)
    results = load_backtest_results()
    stock_trades = results[results["token"] == stock]

    # Creating the plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Close Price"))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA"], mode="lines", name="SMA", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df.index, y=df["Upper_Band"], mode="lines", name="Upper Band", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=df.index, y=df["Lower_Band"], mode="lines", name="Lower Band", line=dict(color="red")))

    # Plotting buy/sell points
    fig.add_trace(go.Scatter(x=stock_trades["date_in"], y=stock_trades["buy_price"], mode="markers",
                             name="Buy", marker=dict(color="blue", size=10, symbol="triangle-up")))
    fig.add_trace(go.Scatter(x=stock_trades["date_out"], y=stock_trades["sell_price"], mode="markers",
                             name="Sell", marker=dict(color="red", size=10, symbol="triangle-down")))

    fig.update_layout(title=f"Bollinger Bands for {stock}", xaxis_title="Date", yaxis_title="Price")

    return render_template("visualization.html", plot=fig.to_html(), trades=stock_trades.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
