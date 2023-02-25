# AlgoBulls Assignment

# --------INSTRUCTIONS--------

In this repository you will be able to see 8 files
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
1. using_postman_files.ipynb
2. using_alphavan_api.ipynb

As the names of these Jupyter Notebook files suggest,
## 1. using_postman_files.ipynb
This file work based on the JSON, CSV files in
the repository which were exported from postman.com. This program
works on GOOGL and AAPL stock data. This Jupyter notebook file follows each 
instruction specified in the "AlgoBulls - Python Developer _ Strategy _ Coding Assignment" 
provided by AlgoBulls. At the end of the program I wrote a code which generated Candlestick
graph for both GOOGL and AAPL data.

## 2. using_alphavan_api.ipynb
This one is used when we want to use Alpha Vantage package
which directly fetches the desired data from Alpha Vantage
(API KEY maybe required but we can still get the data we want without it).
We just have to change the parameters while calling the classes, functions,
methods to "GOOGL" or "AAPL". I included the graph for this program too.

## for_ide.py
You can use for_ide.py in IDLE/IDE this gives the same result except
this program asks at the starting of the program if you want GOOGL data
or AAPL data.

For all the programs I added comments which should explain most of the details.

Feel free to test out these codes.

## Note:
I don't know why but "using_alphavan_api.ipynb" often randomly gets 
errors regarding API calls and running it a few times at the line where
it is stopped gives the proper output.

## Edit:
On searching for the above issue I found that we can make only a specific
amount of API calls hence once the limit is reached it starts producing 
errors. Apparently we can only make 5 API calls for a min, I started executing 
the same line several times by pressing "shift + enter" it is actually giving 
me the desired output but I would  recommend using "using_postman_files.ipynb"

That's it from my side!

# --------Thanks for reading!--------

Please contact me if you have any doubts or found any problem with the code, I will be happy to receive any advices if possible.
E-mail: akkineni.jagadeesh@gmail.com
