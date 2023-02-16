# Importing necessary packages
import json
import os
import pandas as pd
import numpy as np

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
	
	# This method is used to fetch Intraday Historical day data
	def fetch_historical_data(self):
		if choice == "1" or choice == "GOOGL":
			df_csv = pd.read_csv(directory + "\\extended_intraday_GOOGL.csv")
		elif choice == "2" or choice == "AAPL":
			df_csv = pd.read_csv(directory + "\\extended_intraday_AAPL.csv")
		df_csv = df_csv.rename(columns={'time': 'timestamp'})
		return df_csv
		
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

# Creating a class Strategy which processes on Historical day data
class Strategy:
	# Constructor
	def __init__(self, script_data):
		self.script_data = script_data

	# Fetching historical data data frame from ScriptData class
    # Changing the column names of 
    # "indicator" to "indicator_data"
    # "close" to "close_data", here we directly store data from close
	def fetch_intraday_historical_day_data(self):
		a = self.script_data.fetch_historical_data()
		close_values = [i for i in a["close"]]
		b = self.script_data.indicator1(a["timestamp"], a)
		b = b.rename(columns={'indicator': 'indicator_data'})
		for i in range(0, len(a["close"])):
			b["close_data"] = close_values
		return b

	# In this method we calculate BUY, SELL and NO SIGNAL based on 
	# "indicator_data" and "close_data" and append it to a column called "signal"
	def get_signal(self):
		a = self.script_data.fetch_historical_data()
		close_values = [i for i in a["close"]]
		b = self.script_data.indicator1(a["timestamp"], a)
		b = b.rename(columns={'indicator': 'indicator_data'})
		for i in range(0, len(a["close"])):
			b["close_data"] = close_values
		c = {"timestamp": [], "signal" : []}
		for i in range(0, len(b)):
			if float(b["indicator_data"].iloc[i]) < float(b["close_data"].iloc[i]):
				c["timestamp"].append(b["timestamp"][i])
				c["signal"].append("SELL")
			elif float(b["indicator_data"].iloc[i]) > float(b["close_data"].iloc[i]):
				c["timestamp"].append(b["timestamp"][i])
				c["signal"].append("BUY")
			else:
				c["timestamp"].append(b["timestamp"][i])
				c["signal"].append("NO SIGNAL")
		df_03 = pd.DataFrame(c)
		# Removing any row with "NO SIGNAL" and resetting the index
		df_03 = df_03[df_03['signal'] != 'NO SIGNAL'].reset_index(drop=True)
		# Uncomment this incase you want to get the output in excel file
        # df_03.to_excel('output.xlsx', index=True)
		return df_03

# Creating an object for ScriptData class and passing parameter
# as it needs to be initiated for __init(self, script)
script_data = ScriptData(ts_1)

# Creating an object for Strategy class and passing an argument/parameter
strategy_data = Strategy(script_data)

# Calling convert_intradat_data() method with
# data present in fetch_intraday_data()
print(script_data.convert_intraday_data(script_data.fetch_intraday_data(ts_1)))

# Printing out the contents of indicator1 with moving average
print(script_data.indicator1(timestamp= script_data.df["timestamp"], dataf = script_data.df))

# Printing the historical data which is stored in excel file
print(script_data.fetch_historical_data())

# Getting the modified historical to calculate BUY, SELL and GET SIGNAL
print(strategy_data.fetch_intraday_historical_day_data())

# Printing get_signal()
print(strategy_data.get_signal())

# Checking if AAPL or GOOGL is in the data we are processing
print("GOOGL" in data["Meta Data"]["2. Symbol"])
print("AAPL" in data["Meta Data"]["2. Symbol"])
