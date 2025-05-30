from flask import Flask, render_template
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly
import json

app = Flask(__name__)

def fetch_stock_data():
    # Fetch AAPL data (adjust period or interval as per repo)
    stock = yf.Ticker("AAPL")
    data = stock.history(period="1mo", interval="1d")
    data.reset_index(inplace=True)
    return data

def calculate_moving_average(data, window=20):
    # Calculate simple moving average
    data['SMA'] = data['Close'].rolling(window=window).mean()
    return data

def create_plot(data):
    # Create a Plotly candlestick chart
    fig = go.Figure(data=[
        go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='AAPL'
        ),
        go.Scatter(
            x=data['Date'],
            y=data['SMA'],
            line=dict(color='blue', width=2),
            name='20-Day SMA'
        )
    ])
    fig.update_layout(
        title='Apple (AAPL) Stock Price with 20-Day Moving Average',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        xaxis_rangeslider_visible=False
    )
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def home():
    data = fetch_stock_data()
    data = calculate_moving_average(data)
    plot_json = create_plot(data)
    return render_template('index.html', plot_json=plot_json)

if __name__ == '__main__':
    app.run(debug=True)
