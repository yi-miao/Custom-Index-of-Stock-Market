from cnbcfinance.cnbc import Cnbc
import time
import datetime

def get_datetime():
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")  # Get current time (HH:MM:SS)
    date_str = now.strftime("%Y-%m-%d")  # Get current date (YYYY-MM-DD)
    day_str = now.strftime("%A")  # Get current day (Monday, etc.)
    return time_str, date_str, day_str

time_str, date_str, day_str = get_datetime()
    
text_lines = [
    f"Date: {date_str}",
    f"Time: {time_str}",
    f"Day: {day_str}"
]

print(text_lines)
    
# Define stock symbols
symbols = ["STK1", "STK2", "STK3", "STK4"]

# Loop through each symbol to fetch the latest price
prices = {}
for symbol in symbols:
    cnbc = Cnbc(symbol)
    quote = cnbc.get_quote()
    prices[symbol] = float(quote[0]["last"])  # Extract only the latest price
    time.sleep(0.5)    

# Print the latest prices
for symbol, price in prices.items():
    print(f"Current price of {symbol}: {price}")

print(f"STK2/STK3: {round(prices['STK2']/prices['STK3'], 2)}")    
custom_index = round(prices['STK4']*prices['STK2']/(prices['STK3']*prices['STK1']), 2)
print(f"custom index: {custom_index}")