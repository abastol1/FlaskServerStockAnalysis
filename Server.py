from flask import Flask
from flask_cors import CORS, cross_origin
from TwitterSentiment import TwitterClient
from WebScrappingYahooFinance import WebScrapYahooFinance
from flask_ngrok import run_with_ngrok
import pandas as pd

app = Flask(__name__)

# Exposing the localhost(Flask server) to internet using ngrok
run_with_ngrok(app)

CORS(app)

# Ticker name for all the companies used in the mobile application
# Used while scrapping data from Yahoo Finance
companyTicker = {
	'Amazon': 'AMZN',
	'Apple': 'AAPL',
	'Google': 'GOOG',
	'Jefferies': 'JEF',
	'Facebook': 'FB',
	'IBM': 'IBM',
	'HP': 'HPE',
	'Tesla': 'TSLA',
	'Walmart': 'WMT',
	'Microsoft': 'MSFT'
}	

"""
		@app.route('/<nameCompany>', methods=['GET']):getTweetsDetail():

NAME
		
		def getTweetsDetail: Flask Get method to get tweets details 
SYNOPSIS

		@app.route('/<nameCompany>', methods=['GET'])
		def getTweetsDetail(nameCompany):

            /<nameCompany>: server call is made to this url
            methods=['GET']: GET method that returns json object to
            nameCompany: name of the company whose tweets details are extracted

DESCRIPTION

        This is a GET method for flask server. It receives name of a comapany
        through api request. Creates instance of TwitterClient class, calls
        'getTweets' function in TwitterClient by passing number of tweets and]
        name of the company

RETURNS

        Returns tweetDetails. The 'tweetDetails' dictionary contains tweets, 
        					number of positive, negative and neutral tweets

AUTHOR

        Anuj Bastola

DATE

        03:15 PM 09/12/2019

"""
@app.route('/<nameCompany>', methods=['GET'])
def getTweetsDetail(nameCompany):
	print("Company Name: " + nameCompany)
	count = 200
	twitterClient = TwitterClient()
	# Gets all the tweets by filtering out links, unnecessary characters, emojis
	tweetsDetail = twitterClient.getTweets(nameCompany, count)

	# print(tweetsDetail)
	return tweetsDetail


"""
		@app.route('/currentstock/<nameCompany>', methods=['GET']):
		def getCurrentDetail(nameCompany)

NAME
		
		def getCurrentDetail: Flask GET method that contains information
							about current stock of a company
SYNOPSIS

		@app.route('/currentstock/<nameCompany>', methods=['GET']):
		def getCurrentDetail(nameCompany)

            /currentstock/<nameCompany>: server call is made to this url
            methods=['GET']: GET method that returns json object to
            nameCompany: name of the company whose current stock details 
            			 are extracted from Yahoo Finance

DESCRIPTION

        This is a GET method for flask server. It receives name of a comapany
        through api request. Creates instance of WebScrapYahooFinance class by 
        passing company's ticker, calls 'parseData()' function in 
        WebScrapYahooFinance.

RETURNS

        Returns webData. WebData Stores Previous Close, Open, Fifty_two-WK_range, 
        TD_VOLUME, AVERAGE_VOLUME_3MONTH, MARKET_CAP, PE_RATIO, EPS_RATIO, 
        DIVIDEND_AND_YIELD, EX_DIVIDEND_DATE, ONE_YEAR_TARGET_PRICE 

AUTHOR

        Anuj Bastola

DATE

        03:49 PM 09/12/2019

"""
@app.route('/currentstock/<nameCompany>', methods=['GET'])
def getCurrentDetail(nameCompany):
	webscrap = WebScrapYahooFinance(companyTicker[nameCompany])
	# Gets current stock data from WebScrapYahooFinance 
	# Used in mobile application to display company's stock data
	webData = webscrap.parseData()
	# print(webData)
	return webData


"""
		@app.route('/graphdetail/<nameCompany>', methods=["GET"])
		def returnGraphDetail(nameCompany):
		
NAME
		
		def returnGraphDetail: Flask Get method to get datapoints for graph
SYNOPSIS

		@app.route('/graphdetail/<nameCompany>', methods=["GET"])
		def returnGraphDetail(nameCompany):

            /graphdetail<nameCompany>: server call is made to this url
            methods=['GET']: GET method that returns json object to
            nameCompany: name of the company whose datapoints are requested

DESCRIPTION

        This is a GET method for flask server. It receives name of a comapany
        through api request. Reads .csv file from Assets folder and stores the
        content of file in a pandas dataframe. Drops all the columns but Date and
        Close. Iterates over the dataframe and store Date and CLosing price in 
        an array. 
RETURNS

        Returns dataToReturn. 'dataToReturn' contains a array of array[Date, Close]

AUTHOR

        Anuj Bastola

DATE

        05:29 PM 09/12/2019

"""

@app.route('/graphdetail/<nameCompany>', methods=["GET"])
def returnGraphDetail(nameCompany):
	
	ticker = companyTicker[nameCompany]

	# All the data in csv files are scraped from Yahoo Finance and
	# stored in Assets folder with ticker as filename and .csv as extension
	filePath = "./Assets/" + str(ticker) + ".csv"
	print("File Path: " + str(filePath)) 
	df = pd.read_csv(filePath)
	try:
		# Dropping all other columns, graph and prediction are done with Closing Price and Date
		df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1, inplace=True)
		# df['Date'] = pd.to_datetime(df.Date, format="%m/%d/%Y")
	except Exception as e:
		raise e

	print(df.head())

	dateAndClose = []

	# Iterate over all the rows and get only Date and Close column
	# Append it to dateAndClose array
	for index, row in df.iterrows():
		tempData = [ row['Date'], row['Close']]
		dateAndClose.append(tempData)
		# tempData[index] = tempData
	print("------------------------------------")

	dataToReturn = {}
	dataToReturn['Data'] = dateAndClose
	# can only send JSON object over this server
	return dataToReturn

if __name__ == '__main__':
   app.run()