# NUMPY and Pandas for data preprocessing and cleaning
import numpy as numpy
import pandas as pd 

# Visualization library
import matplotlib.pyplot as plt

# Machine learning algorithm
# SVR is an regression algorihtm
from sklearn.svm import SVR

from datetime import date
from Database import DataBase

class Prediction(object):

	def __init__(self, ticker):
		self.df = pd.read_csv('./stock_data/' + ticker + '.csv')
		self.ticker = ticker
		# self.ticker =


	def SplitData(self):
		dates = []
		prices = []

		# Get all the data except for the last row
		self.df = self.df.head(len(self.df) - 1)

		datesDF = self.df.loc[:, 'Date']
		closeDF = self.df.loc[:, 'Close']

		# splitting the dataset into a new data for Date column
		for date in datesDF:
			dates.append([int(date.split('-')[2])])

		# splitting the dataset into a new data for Close price column
		for close in closeDF:
			prices.append(float(close))

		return [dates, prices]

	def predictClosePrice(self, dates, prices, topredict):
		print("To predict: ", topredict)

		# Creating model for SVR with Radial Basis Function(rbf) kernel
		rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)

		# Training models based on dates and closing prices
		rbf.fit(dates, prices)

		plt.plot(dates, prices, color='blue', label="Actual Stock")
		plt.plot(dates, rbf.predict(dates), color='red', label="RBF Model Prediction")


		plt.xlabel("Stock Traded Date")
		plt.ylabel("Closing Price")
		plt.title("Support Vector Regression")
		plt.legend()
		plt.show()

		return rbf.predict(topredict)[0]


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

    # Create table in database if already not exists
    database = DataBase()
    database.dropEverything()
    database.createDatabase()


	# Looping over every ticker name
    todayDate = date.today()
    nextDay = todayDate.day + 1
    for ticker in companyTicker: 
    	prediction = Prediction(ticker)
    	datesPrices = prediction.SplitData()
    	predictedClose = prediction.predictClosePrice(datesPrices[0], datesPrices[1], [[nextDay]])
    	print("Predicted Close: ", predictedClose)
    	database.storePrediction(ticker, predictedClose)
    	print("From Database: Ticker: " + ticker + " Predicted: " + database.getPredictedClose(ticker))


if __name__ == "__main__": 
    # calling main function 
    main() 