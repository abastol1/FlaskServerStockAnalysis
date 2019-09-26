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
def cleanTweets():

NAME
		
		def cleanTweets(): Cleans Tweet by applying regular expressions
SYNOPSIS

        def cleanTweets(self, tweet)

            self: Represents the instance of the class
            tweet: Tweet extracted from Twitter

DESCRIPTION

        This is a function that takes a single tweet as a parameter and
        applies multiple regular expression to clean tweet. First it applies 
		regular expression to remove URLs from tweet. It then removes all
		RT||CC(retweet symbol) from tweet. It then removes all the hashtags
		from tweet. After that, it removes mentioned username if any. Also,
		removes all the unnecessary characters and punctuations. Finally
		removes emojis from tweet

RETURNS

        Returns tweet after cleaning, only text

AUTHOR

        Anuj Bastola

DATE

        10:15 PM 08/28/2019

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
def cleanTweets():

NAME
		
		def cleanTweets(): Cleans Tweet by applying regular expressions
SYNOPSIS

        def cleanTweets(self, tweet)

            self: Represents the instance of the class
            tweet: Tweet extracted from Twitter

DESCRIPTION

        This is a function that takes a single tweet as a parameter and
        applies multiple regular expression to clean tweet. First it applies 
		regular expression to remove URLs from tweet. It then removes all
		RT||CC(retweet symbol) from tweet. It then removes all the hashtags
		from tweet. After that, it removes mentioned username if any. Also,
		removes all the unnecessary characters and punctuations. Finally
		removes emojis from tweet

RETURNS

        Returns tweet after cleaning, only text

AUTHOR

        Anuj Bastola

DATE

        10:15 PM 08/28/2019

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
def cleanTweets():

NAME
		
		def cleanTweets(): Cleans Tweet by applying regular expressions
SYNOPSIS

        def cleanTweets(self, tweet)

            self: Represents the instance of the class
            tweet: Tweet extracted from Twitter

DESCRIPTION

        This is a function that takes a single tweet as a parameter and
        applies multiple regular expression to clean tweet. First it applies 
		regular expression to remove URLs from tweet. It then removes all
		RT||CC(retweet symbol) from tweet. It then removes all the hashtags
		from tweet. After that, it removes mentioned username if any. Also,
		removes all the unnecessary characters and punctuations. Finally
		removes emojis from tweet

RETURNS

        Returns tweet after cleaning, only text

AUTHOR

        Anuj Bastola

DATE

        10:15 PM 08/28/2019

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
	return dataToReturn

if __name__ == '__main__':
   app.run()