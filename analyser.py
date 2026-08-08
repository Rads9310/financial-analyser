import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

def stock_summary(sybol):
    # 1. Get stock data
    #symbol = 'AAPL'
    stock = yf.Ticker(symbol)

    # Fetch 1 year of data (so 200-day average works)
    data = stock.history(period="1y")  # ← Changed from "6mo" to "1y"

    # 2. Remove any rows with NaN (e.g., weekends/holidays)
    data = data.dropna()  #This removes today if market is closed

    # 3. Show data
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    formatted_data = pd.concat([data.head(), data.tail()])
    print(tabulate(formatted_data, headers='keys', tablefmt='psql'))

    # 4. Show what we got
    print(f"✅ Loaded {len(data)} days of data")
    print(f"📅 From: {data.index[0].date()} to {data.index[-1].date()}")

    # 5. Calculate moving averages
    data['SMA_50'] = data['Close'].rolling(50).mean()
    data['SMA_200'] = data['Close'].rolling(200).mean()

    # 6. Calculate daily returns
    data['Daily_Return'] = data['Close'].pct_change()

    # 7. Print summary
    print("\n📊 Summary:")
    print(f"💰 Current Price: ${data['Close'].iloc[-1]:.2f}")
    print(f"📈 50-Day Average: ${data['SMA_50'].iloc[-1]:.2f}")
    print(f"📈 200-Day Average: ${data['SMA_200'].iloc[-1]:.2f}")
    print(f"📉 Volatility: {data['Daily_Return'].std() * 100:.2f}%")

# 8. Draw the chart
def draw_chart(data,symbol):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Close'], label='Price', color='blue', linewidth=1)
    plt.plot(data.index, data['SMA_50'], label='50-Day Avg', color='orange', linewidth=2)
    plt.plot(data.index, data['SMA_200'], label='200-Day Avg', color='red', linewidth=2)
    plt.title(f'{symbol} Stock Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    #Enable to save as png file
    #plt.savefig(f'{symbol}_analysis.png')



    #Enable to save data as file
    # 9. Export to CSV
    #data.to_csv(f'{symbol}_data.csv')

    #print(f"\n✅ Chart saved as '{symbol}_analysis.png'")
    #print(f"✅ Data saved as '{symbol}_data.csv'")

# 10. Multiple Stocks Analysis
def stock_comparison(stocks):
    print("\n" + "=" * 75)
    print(" MULTIPLE STOCKS COMPARISON TABLE")
    print("=" * 75)



    # Store data in a list for table formatting
    results = []

    for symbol in stocks:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1y")
        data = data.dropna()

        data['SMA_50'] = data['Close'].rolling(50).mean()
        data['SMA_200'] = data['Close'].rolling(200).mean()
        data['Daily_Return'] = data['Close'].pct_change()

        results.append([
            symbol,
            f"${data['Close'].iloc[-1]:.2f}",
            f"${data['SMA_50'].iloc[-1]:.2f}",
            f"${data['SMA_200'].iloc[-1]:.2f}",
            f"{data['Daily_Return'].std() * 100:.2f}%"
        ])

    # Print as a formatted table using tabulate

    headers = ['Stock', 'Current Price', '50-Day Avg', '200-Day Avg', 'Volatility']
    print(tabulate(results, headers=headers, tablefmt='grid'))

    plt.show()

if __name__ == '__main__':

    stocks = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA','DIA']

    stock_comparison(stocks)
    symbol = ""
    while symbol not in stocks:
        symbol = input("What stock would you like to look at? ")

    stock_summary(symbol)



