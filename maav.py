from datetime import datetime
import os
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time
import matplotlib.pyplot as plt
import argparse
import matplotlib.dates as mdates

class MAAV:
    def __init__(self):
        today_date = datetime.today().strftime('%Y%m%d')
        self.filename = f'histodata_{today_date}.csv'
        self.df_pivoted = None

    def data_downloader(self):
        api_key = 'your_alpha_vantage_api_key'
        ts = TimeSeries(key=api_key, output_format='pandas')
        tickers = ['STK1', 'STK2', 'STK3', 'STK4'] 
        data_frames = {}
        for ticker in tickers:
            df, meta_data = ts.get_daily(symbol=ticker, outputsize='full')
            df.rename(columns={"1. open": "Open"}, inplace=True)
            df.rename(columns={"2. high": "High"}, inplace=True)
            df.rename(columns={"3. low": "Low"}, inplace=True)
            df.rename(columns={"4. close": "Close"}, inplace=True)
            df.rename(columns={"5. volume": "Volume"}, inplace=True)
            df.index = pd.to_datetime(df.index) 
            one_year_ago = pd.Timestamp.today() - pd.DateOffset(years=1)
            df = df.loc[df.index >= one_year_ago]
            df.ffill(inplace=True)
            data_frames[ticker] = df
            print(data_frames[ticker].head(5))
            time.sleep(1)

        valid_tickers = [ticker for ticker in tickers if ticker in data_frames]
        if valid_tickers:
            all_data = pd.concat(data_frames, keys=valid_tickers)
            all_data.to_csv(self.filename)
        else:
            print("No valid data downloaded today. Consider loading from a previous file.")
        
    def file_loader(self):
        if os.path.exists(self.filename):
            print(self.filename)
            column_names = ["Symbol", "Date", "Open", "High", "Low", "Close", "Volume"]
            data_frames = pd.read_csv(self.filename, names=column_names, header=None, parse_dates=True, skiprows=1)
            self.df_pivoted = data_frames.pivot(index="Date", columns="Symbol", values=["Open", "High", "Low", "Close", "Volume"])

            print("Data loaded from file: ", self.filename)

    def data_visualizer(self):
        # Create custom index calculation
        custom_index = self.df_pivoted[("Close", "SMH")] * self.df_pivoted[("Close", "XLK")]/(self.df_pivoted[("Close", "UUP")] * self.df_pivoted[("Close", "XLU")]) # * df_pivoted[("Close", "VXX")])
        last_date_value = custom_index.iloc[-1] # custom_index.tail(1).values[0]
        last_date = custom_index.index[-1]

        # Calculate moving average & Bollinger Bands
        window = 20
        custom_index_ma = custom_index.rolling(window).mean()
        custom_index_std = custom_index.rolling(window).std()
        upper_band = custom_index_ma + (custom_index_std * 2)
        lower_band = custom_index_ma - (custom_index_std * 2)

        # +/- two times standard deviations
        mean_value = custom_index.mean()
        std_value = custom_index.std()
        plus_2_sigma = mean_value + 2 * std_value
        minus_2_sigma = mean_value - 2 * std_value

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

        # Time Series Chart
        ax1.xaxis.set_major_locator(mdates.MonthLocator())  
        ax1.plot(custom_index, label='Custom Index')
        ax1.plot(custom_index_ma, label='20-Day MA', color='orange')
        ax1.plot(upper_band, label='Upper Band', color='lightgreen', linestyle='--')
        ax1.plot(lower_band, label='Lower Band', color='lightgreen', linestyle='--')
        ax1.set_title('Custom Index - Time Series')
        ax1.axvline(last_date, color='red', linestyle='dashed', linewidth=1)
        ax1.text(last_date, custom_index.max()*0.9, f'Last Date\n {last_date}', color='red', fontsize=10, ha='right')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Index Value')
        ax1.legend()
        ax1.grid(True, which='both', linestyle='--')

        # Histogram Chart
        n, bins, patches = ax2.hist(custom_index, bins=50, alpha=0.75, color='blue', edgecolor='black')
        ax2.axvline(last_date_value, label='Last Value', color='red', linestyle='dashed', linewidth=1)
        ax2.axvline(minus_2_sigma, label='-2 Sigma', color='lightgreen', linestyle='dashed', linewidth=1)
        ax2.axvline(plus_2_sigma, label='+2 Sigma', color='lightgreen', linestyle='dashed', linewidth=1)
        ax2.text(last_date_value, max(n)*0.9, f'Last Value\n {last_date_value:.2f}', color='red', fontsize=10, ha='right')
        ax2.set_title('Custom Index - Histogram')
        ax2.set_xlabel('Index Value')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, which='both', linestyle='--')

        plt.tight_layout()
        fig.canvas.manager.set_window_title('Market Analysis (12 Months)')
        plt.show()

    def run(self):
        # Create the argument parser
        parser = argparse.ArgumentParser(description="Stock Data Downloader")

        # Add switches (-d for download, -f for file input)
        parser.add_argument("-d", "--download", action="store_true", help="Download new market data")
        parser.add_argument("-f", "--file", action="store_true", help="Load latest market data file")

        # Parse the arguments
        args = parser.parse_args()

        # Handle the switches
        if args.download:
            self.data_downloader()
            self.file_loader()
            self.data_visualizer()

        if args.file:
            self.file_loader()
            self.data_visualizer()
        
if __name__ == '__main__':
    ma = MAAV()
    ma.run()
