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

# I have used non-linear SVR model for my prediction. 
# Non-linear SVR transforms data into a higher dimensional feature space 
# to make it possible to perform linear separation. 
# The reason I decided to use SVR model is to make non-linear regression, 
# i.e. fitting a curve rather than a line. 
# The model is represented as combinations of the training points rather than a function of the features and some weights.  


class Prediction(object):

	# Reads data from CSV file into a dataframe and 
	# initializes the dataframe and ticker in class variables. 
	def __init__(self, ticker):
		self.df = pd.read_csv('./stock_data/' + ticker + '.csv')
		self.ticker = ticker
		# self.ticker =

	# This function splits datasets into two different data sets ‘dates’ and ‘prices. 
	# ‘date’ and ‘prices’ are given value from CSV file. 
	# The CSV file is updated every day. 
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


	# This function creates Support Vector Regression model 
	# with RBF (Radial Basis Function) kernel. 
	# It trains the model with the dates and prices data. 
	# It then plots a graph with initial datasets and predicted datasets. 
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


"""
	The main function first initializes Database class. 
	It then drops the old data from the database and creates a new table with no data. 
	It then does prediction for all the companies by passing tickerName and nextDay number. 
	Once the prediction is done, it calls ‘database.storePrediction’ function 
	which stores tickerName and prediction on the ElephantSQL database

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