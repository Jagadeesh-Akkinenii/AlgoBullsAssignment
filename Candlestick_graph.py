# Importing necessary packages
import json
import os
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

# Getting path to our directory/folder
directory = os.getcwd()

# Type 1 or GOOGL for GOOGL stock data and
# type 2 or AAPL for AAPL stock data
choice = input("ENTER YOUR CHOICE\n1. GOOGL\n2. AAPL\n")

if choice == "1" or choice == "GOOGL":
	# Loading the JSON file which was downloaded from postman.com
    with open(directory + "\\response_GOOGL.json", "r") as f:
        data = json.load(f)
elif choice == "2" or choice == "AAPL":
    with open(directory+"\\response_AAPL.json", "r") as f:
        data = json.load(f)
else:
    print("INVALID ENTRY")

# Saving the loaded content in a variable
ts_1 = data

# Creating a class ScriptData that fetches stock data
class ScriptData:
	# Constructor
	def __init__(self, script):
		self.script = script
		self.fetch_intraday_data(self.script)
		self.df = self.convert_intraday_data(self.data)
		self.df["symbol"] = self.script

	# Fetching intraday stock data
	def fetch_intraday_data(self, script):
		self.data = ts_1
		return self.data
		
	# Tis method converts the raw data that has been fetched
    # by fetch_intraday_data method and converts it into a Data Frame
	def convert_intraday_data(self, data):
		self.data_list = []
		for timestamp, items in data["Time Series (5min)"].items():
			open_item = float(items["1. open"])
			high_item = float(items["2. high"])
			low_item = float(items["3. low"])
			close_item = float(items["4. close"])
			volume = int(items["5. volume"])
			self.data_list.append([timestamp, open_item, high_item, low_item, close_item, volume])
		df = pd.DataFrame(self.data_list, columns=[ "timestamp", "open", "high", "low", "close", "volume"])
		df["timestamp"] = pd.to_datetime(df["timestamp"])
		return df

	# This method calculates moving averages in close/close_data
    # and saves it in indicator column
	def indicator1(self, timestamp, dataf, timeperiod= 5):
		indicator_data = []
		final_output = {"timestamp": [], "indicator" : []}
		upcount = 0
		downcount = timeperiod - 1
		# Below part is where the moving average calculation takes place
		while downcount < len(dataf):
			cal_temp = 0
			# This for_loop loops from range upcount to downcount + 1
            # In this case it goes from 0 to 5+1 that means 0 - 5 and 
            # both upcount and downcount increases for each while loop
			for i in range(upcount, downcount + 1):
				cal_temp = float(dataf["close"][i]) + cal_temp
			final_temp = cal_temp/timeperiod
			# Appending the calculated data to a list
			indicator_data.append(final_temp)
			if downcount + 1 >= len(dataf):
				break
			upcount += 1
			downcount += 1
		# Appending timestamp column to a dictionary
		for i in range(0, len(dataf)):
			final_output["timestamp"].append(dataf["timestamp"][i])
		# Appending moving average(final_temp) column to a dictionary
		for i in range(0, len(dataf)):
			if i < timeperiod - 1:
				final_output["indicator"].append("NaN")
			else:
				final_output["indicator"].append(
                    indicator_data[i-timeperiod + 1])
		# Finally converting the dictionary to a DataFrame with columns
        # "timestamp" and "indicator"
		df_1 = pd.DataFrame(final_output)
		df_1.fillna(value= np.nan, inplace = True)
		return df_1

	# Overloading methods
	def __getitem__(self, index):
		return self.df.loc[index]

	def __setitem__(self, index, value):
		self.df.iloc[index] = value

	def __contains__(self, value):
		return value in self.df['symbol'].values


# Creating an object for ScriptData class and passing parameter
# as it needs to be initiated for __init(self, script)
script_data = ScriptData(ts_1)

df_candle = script_data.convert_intraday_data(script_data.fetch_intraday_data(ts_1))

# sort the dataframe by timestamp
df_candle = df_candle.sort_values('timestamp')

# create a new dataframe with the required columns for the candlestick chart
ohlc_df = pd.DataFrame(index=df_candle.index, columns=['open', 'high', 'low', 'close'])
ohlc_df['open'] = df_candle['close'].shift(1)
ohlc_df['high'] = df_candle['close']
ohlc_df['low'] = df_candle['close']
ohlc_df['close'] = df_candle['close']

# create the candlestick chart using plotly
import plotly.graph_objects as go

fig = go.Figure(data=[go.Candlestick(x=df_candle['timestamp'],
                                     open=ohlc_df['open'],
                                     high=ohlc_df['high'],
                                     low=ohlc_df['low'],
                                     close=ohlc_df['close'])])

fig.show()