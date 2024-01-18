import numpy as np
import pandas as pd

# Set display option to show all columns
pd.set_option('display.max_columns', None)

# YOU WILL NEED TO INCLUDE YOUR OWN DATA HERE
daily = pd.read_csv('prices_data.csv') # Data on the daily timeframe (from yfinance)
intra = pd.read_csv('AAPL_intraday_data.csv') # Intraday data (from Polygon)

def calculate_rsi(col, period=14):
    delta = col.diff()

    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

intra['rsi_14'] = calculate_rsi(intra['Close'], period=14)
print(intra.dropna().head())