import yfinance as yf

def fetch_latest_close_price():
    # Ticker symbol for the 13 Week Treasury Bill
    ticker_symbol = "^IRX"

    # Fetch the data using yfinance
    treasury_bill_data = yf.download(ticker_symbol)

    # Get the latest close price
    latest_close_price = treasury_bill_data['Close'].iloc[-1]

    return latest_close_price

if __name__ == "__main__":
    try:
        latest_close_price = fetch_latest_close_price()
        rounded_close_price = round(latest_close_price, 2)
        print(rounded_close_price)
    except Exception as e:
        print("An error occurred:", e)
