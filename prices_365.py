from polygon import RESTClient
import json
import pandas as pd
import time

from datetime import datetime

# Get the current time
current_time = datetime.now().time()

print("Start time:", current_time)

# Polygon Data 1 minute bars

ticker = 'AAPL'
start_date = '2021-11-14'
end_date = '2023-11-22'  # Adjust the end date as needed

rename_cols = {
    'o': 'Open',
    'l': 'Low',
    'h': 'High',
    'c': 'Close',
    'v': 'Volume',
    'vw': 'vwap',
}

client = RESTClient('c5hSVx2pJLI3t5M1ZIVHPr9LmmJpitMe')

def get_intraday(ticker, client, start_date, end_date, rename_cols):
    '''
    Obtain intraday data for a single ticker within a date range
    '''
    prices = client.get_aggs(
        ticker,
        timespan='minute',
        multiplier=1,
        from_=start_date,
        to=end_date,
        adjusted=True,
        raw=True,
    )

    json_response = json.loads(str(prices.data, 'utf-8'))

    flattened_data = pd.json_normalize(json_response['results'])
    df = pd.DataFrame(flattened_data)
    df['timestamp'] = pd.to_datetime(df['t'], unit='ms', origin='unix')
    df['Date'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')

    df = df[
        (df['timestamp'].dt.time >= pd.Timestamp('14:30:00').time())
        & (df['timestamp'].dt.time <= pd.Timestamp('21:00:00').time())
    ]

    df = df.rename(columns=rename_cols)
    df['ticker'] = ticker

    return df[['Date', 'timestamp', 'ticker'] + list(rename_cols.values())].reset_index(drop=True)

# Generate date range for the specified ticker and date range
date_range = pd.date_range(start=start_date, end=end_date, freq='B')
cases = pd.DataFrame({
    'ticker': [ticker] * len(date_range),
    'Date': date_range.strftime('%Y-%m-%d')
})

dfs = []

for n, row in cases.iterrows():
    # You can remove this if statement, if you have bought a data package
    if n != 0 and n % 5 == 0:
        time.sleep(61)

    dfs.append(get_intraday(row['ticker'], client, start_date, end_date, rename_cols))

df = pd.concat(dfs)
print(df)

# Export the DataFrame to a CSV file
csv_filename = f"{ticker}_intraday_data_combined.csv"
df.to_csv(csv_filename, index=False)
print(f"\nData exported to {csv_filename}")
print("End time:", current_time)