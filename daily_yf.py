import yfinance as yf

# Specify the ticker symbol and date range
ticker = 'AAPL'
start_date = '2022-01-01'
end_date = '2022-12-31'

# Download daily data
df = yf.download(ticker, start=start_date, end=end_date)

# Display the downloaded data
print(df.head())

# Export the data to a CSV file
csv_filename = f"{ticker}_daily_data.csv"
df.to_csv(csv_filename, index=False)
print(f"\nData exported to {csv_filename}")
