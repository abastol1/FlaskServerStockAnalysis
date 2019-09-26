import pandas_datareader.data as web
import os
import datetime
import time
from datetime import date

class ScrapStockHistory(object):

    def __init__(self, tickers, startDate, endDate):
        self.tickers = tickers
        self.startDate = startDate
        self.endDate = endDate


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
    def downloadStockData(self):

        # tracking the number of requests made to yahoo finance
        # Yahoo Finance might block our access to data if a large number of requests are made at same time
        # so the program sleeps for 10 seconds after 50 requests are made
        count = 1

        # Creates a folder named stock_data if it doesn't exits
        # Everytime a request is made for a company, the returned data is stored in a .csv file
        directory = 'stock_data'
        if not os.path.exists(directory):
            os.makedirs(directory)


        data = {}

        for ticker in self.tickers:
            filename = directory+'/'+ticker+'.csv'
            data[ticker] = web.DataReader(ticker,"yahoo",self.startDate, self.endDate)
            data[ticker].to_csv(filename)
            count  = count + 1
            if count % 50 == 0:
                time.sleep(10)
        return

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
def main():
    companyTicker = {
        'AMZN',     # Amazon
        'AAPL',     # Apple
        'GOOG',     # Google
        'JEF',      # Jefferies
        'FB',       # Facebook
        'IBM',      # IBM
        'HPE',      # Hawlett Packard Enterprise
        'TSLA',     # Tesla
        'WMT',      # Walmart
        'MSFT'      # Microsoft Cooperation
    }
    todayDate = date.today()

    # Day from where 
    startDate = '%s-%s-%s' % (todayDate.month, todayDate.day, (todayDate.year - 1))
    # day till which the data will be gathered
    todayDate = '%s-%s-%s' % (todayDate.month, todayDate.day, todayDate.year)
    # print("End Date: " + str(todayDate))
    # print("Start Date: " + str(startDate))

    ScrapHistoryData = ScrapStockHistory(companyTicker, startDate, todayDate)

    ScrapHistoryData.downloadStockData()

if __name__ == '__main__':
    main()
    # download_data(tickers,start,end)