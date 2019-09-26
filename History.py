import pandas_datareader.data as web
import os
import datetime
import time
from datetime import date

class ScrapStockHistory(object):

    # Tickers: Stores tickers for all the company names
    # startDate: startDate from which stock data is download
    # endDate: All stock data withing startDate and endDate are
                # recorded
    def __init__(self, tickers, startDate, endDate):
        self.tickers = tickers
        self.startDate = startDate
        self.endDate = endDate


    """
    def downloadStockData():

    NAME
            
            def downloadStockData(): Web Scraps all the yahoo finance 
                                    data of a comapany(one year data)
    SYNOPSIS

            def cleanTweets(self, tweet)

                self: Represents the instance of the class

    DESCRIPTION
            
            This function downloads stock history of one year, creates
            a folder called stock_data, and creates .csv file with 
            stock data in the file. For security reason, request
            is sent 50 times, and the program sleeps for 10 seconds.
            It avoids Yahoo Finance from blocking access to stock data

    RETURNS

            Returns nothing

    AUTHOR

            Anuj Bastola

    DATE

            10:17 PM 09/12/2019

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
def main():

NAME
        
        def main: Specifies enddate and startdate and calls
                    downloadStockData function 
SYNOPSIS

        def main


DESCRIPTION

        This is a main function for ScrapStockHistory class. It stores
        ticker of each company. Specifies today's date as endDate and
        startDate one year until today. Initializes object for 
        ScrapStockHistory class and calls the downloadStockDate function

RETURNS

        None

AUTHOR

        Anuj Bastola

DATE

        11:19 PM 09/12/2019

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