# AlgoBulls Assignment

# --------INSTRUCTIONS--------

In this repository you will be able to see 10 files
excluding this file.

## requirements.txt
The requirements.txt contains all the necessary packages
that can be quickly installed.
Once the virtual environment has been created and activated which 
can be done as follows,
"env\Scripts\activate.bat" this is for windows cmd(Change env with
the name of your venv name). Now type "pip install - r requirements.tx" 
in cmd to quickly install all the necessary packages to run these programs.

The main files are as follows
1. with_alphavan_api.ipynb
2. AAPL_postman_collection.ipynb
3. GOOGL_postman_collection.ipynb

As the names of these Jupyter Notebook files suggest,
## 1. with_alphavan_api.ipynb
The first one is used when we want to use Alpha Vantage package
which directly fetches the desired data from Alpha Vantage
(API KEY maybe required but we can still get the data we want without it).
We just have to change the parameters while calling the classes, functions,
methods to "GOOGL" or "AAPL".

## 2. AAPL_postman_collection.ipynb
The second and third files work based on the JSON, CSV files in
the repository which were exported from postman.com. This program
works on AAPL stock data.

## 3. GOOGL_postman_collection.ipynb
This one is completely similar to 2nd file except this one works on 
GOOGL stock data.

## for_ide.py
You can use for_ide.py in IDLE/IDE this gives the same result except
this program asks at the starting of the program if you want GOOGL data
or AAPL data.

## candlestick_graph.py
In this program after we select an option from the given i.e, "GOOGL"
and "AAPL" it fetches the intraday data and plots a candlestick graph.

For all the programs I added comments which should explain most of the details.

Feel free to test out these codes.

Note:
I don't know why but "with_alphavan_api.ipynb" often randomly gets 
errors regarding API calls and running it a few times gives the
proper output I am assuming its because of some issue while fetching
data from Alpha Vantage.

That's it from my side!

# --------Thanks for reading!--------

Please contact me if you have any doubts or found any problem with the code, I will be happy to receive any advices if possible.
E-mail: akkineni.jagadeesh@gmail.com
