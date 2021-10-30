# Frimplestatic Trader (Free Simple and Static)

I couldn't find a free trading platform, so I implemented one myself.

The tool plots candlestick charts with the following settings:

- 36 months
- EMA(9) - Exponential Moving Average 9 periods
- EMA(21)
- SMA(200) - Simple Moving Average 200 periods
- Range Selector (1w, 1m, 6m, 1y, YTD)

The data comes from Yahoo!Finance, so you need to search tickers as shown there.

Example: <a href="https://finance.yahoo.com/quote/AAPL/history/" target="_blank">AAPL</a>

Windows users can start it with **start.bat** script.

### Setup
Python 3

Jupyter Notebook

Required Libraries:
- pandas
- pandas-datareader
- plotly
