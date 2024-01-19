import argparse
import yfinance as yf

def download_stock_data(ticker, start_date, end_date, csv_path):
    # Download daily data
    df = yf.download(ticker, start=start_date, end=end_date)

    # Display the downloaded data
    print(df.head())

    # Export the data to a CSV file
    df.to_csv(csv_path, index=False)
    print(f"\nData exported to {csv_path}")

if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Download stock data from Yahoo Finance.")

    # Add command-line arguments
    parser.add_argument('--ticker', required=True, help="Stock ticker symbol")
    parser.add_argument('--start', required=True, help="Start date for data download (YYYY-MM-DD)")
    parser.add_argument('--end', required=True, help="End date for data download (YYYY-MM-DD)")
    parser.add_argument('--path', required=True, help='Path to save the CSV file')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function with the provided arguments
    download_stock_data(ticker=args.ticker, start_date=args.start, end_date=args.end, csv_path=args.path)
