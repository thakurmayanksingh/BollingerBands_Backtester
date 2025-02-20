# Importing libraries
from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go

app = Flask(__name__, template_folder="templates_v2")
RESULTS_FILE = "backtest_results.csv"


# Function to load backtest results from CSV
def load_backtest_results():
    df = pd.read_csv(RESULTS_FILE)
    return df


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/visualize", methods=["GET"])
def visualize():
    # Loading only the backtest results
    results = load_backtest_results()

    # Creating a Plotly figure to visualize the trades.
    # Each trade is shown as a line connecting the buy and sell points.
    fig = go.Figure()
    for idx, trade in results.iterrows():
        fig.add_trace(go.Scatter(
            x=[trade["date_in"], trade["date_out"]],
            y=[trade["buy_price"], trade["sell_price"]],
            mode="lines+markers",
            name=trade["token"],
            text=[f"Buy: {trade['buy_price']}", f"Sell: {trade['sell_price']}"],
            hovertemplate="Date: %{x}<br>Price: %{y}"
        ))

    fig.update_layout(
        title="Backtest Trade Visualization",
        xaxis_title="Date",
        yaxis_title="Price"
    )

    # Rendering the visualization page with the plot and trade table
    return render_template("visualization.html", plot=fig.to_html(), trades=results.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
