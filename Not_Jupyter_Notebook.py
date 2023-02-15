import json
import os
import pandas as pd

directory = os.getcwd()

choice = input("ENTER YOUR CHOICE\n1. GOOGL\n2. AAPL\n")

if choice == "1" or choice == "GOOGL":
    with open(directory + "\\response.json", "r") as f:
        data = json.load(f)
elif choice == "2" or choice == "AAPL":
    with open(directory+"\\response_AAPL.json", "r") as f:
        data = json.load(f)
else:
    print("INVALID ENTRY")

ts_1 = data

class ScriptData:
	def __init__(self, script):
		self.script = script
		self.fetch_intraday_data(self.script)
		self.df = self.convert_intraday_data(self.data)
		self.df["symbol"] = self.script

	def fetch_intraday_data(self, script):
		self.data = ts_1
		return self.data
	
	def fetch_historical_data(self):
		# Get json object with the intraday data
		if choice == "1" or choice == "GOOGL":
			df_csv = pd.read_csv(directory + "\\extended_intraday_GOOGL.csv")
		elif choice == "2" or choice == "AAPL":
			df_csv = pd.read_csv(directory + "\\extended_intraday_AAPL.csv")
		df_csv = df_csv.rename(columns={'time': 'timestamp'})
		return df_csv
		
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

	def indicator1(self, timestamp, dataf, timeperiod= 5):
		indicator_data = []
		final_output = {"timestamp": [], "indicator" : []}
		upcount = 0
		downcount = timeperiod - 1
		while downcount < len(dataf):
			cal_temp = 0
			for i in range(upcount, downcount + 1):
				cal_temp = float(dataf["close"][i]) + cal_temp
			final_temp = cal_temp/timeperiod
			indicator_data.append(final_temp)
			if downcount + 1 >= len(dataf):
				break
			upcount += 1
			downcount += 1
		for i in range(0, len(dataf)):
			final_output["timestamp"].append(dataf["timestamp"][i])
		for i in range(0, len(dataf)):
			if i < timeperiod - 1:
				final_output["indicator"].append("NaN")
			else:
				final_output["indicator"].append(
                    indicator_data[i-timeperiod + 1])
		df_1 = pd.DataFrame(final_output)
		df_1.fillna(value= pd.np.nan, inplace = True)
		return df_1

	def __getitem__(self, index):
		return self.df.loc[index]

	def __setitem__(self, index, value):
		self.df.iloc[index] = value

	def __contains__(self, value):
		return value in self.df['symbol'].values


class Strategy:
	
	def __init__(self, script_data):
		self.script_data = script_data

	def fetch_intraday_historical_day_data(self):
		a = self.script_data.fetch_historical_data()
		close_values = [i for i in a["close"]]
		b = self.script_data.indicator1(a["timestamp"], a)
		b = b.rename(columns={'indicator': 'indicator_data'})
		for i in range(0, len(a["close"])):
			b["close_data"] = close_values
		return b

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
		df_03 = df_03[df_03['signal'] != 'NO SIGNAL'].reset_index(drop=True)
		df_03.to_excel('output.xlsx', index=True)
		# df_03.to_excel('output.xlsx', index=True)
		return df_03


script_data = ScriptData(ts_1)
strategy_data = Strategy(script_data)

print(script_data.convert_intraday_data(script_data.fetch_intraday_data(ts_1)))
print(script_data.indicator1(timestamp= script_data.df["timestamp"], dataf = script_data.df))
print(script_data.fetch_historical_data())
print(strategy_data.fetch_intraday_historical_day_data())
print(strategy_data.get_signal())
print("GOOGL" in data["Meta Data"]["2. Symbol"])
print("AAPL" in data["Meta Data"]["2. Symbol"])
