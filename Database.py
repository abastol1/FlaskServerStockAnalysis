# Accessing POSTGRESQL database
import psycopg2
from urllib.parse import urlparse, uses_netloc

uses_netloc.append("postgres")
url = urlparse('postgres://hnxjuics:HrZVGMmGgSwtR7lHmbo61qA_cG1c-zlB@salt.db.elephantsql.com:5432/hnxjuics')


class DataBase(object):

	def __init__(self):
		self.conn = psycopg2.connect(database=url.path[1:],
			user = url.username,
			password = url.password,
			host = url.hostname,
			port = url.port
			)

	# Drops table from a database. 
	# Every morning, the table is dropped and new table with a new prediction is created. 
	def dropEverything(self):
		cursor = self.conn.cursor()
		cursor.execute("DROP TABLE MARKET")
		self.conn.commit()
		
	# When Prediction.py is run, it drops the old table and creates a new one. 
	# It creates a table with two-column, ticker column which is primary key for the database and prediction column
	def createDatabase(self):
		cursor = self.conn.cursor()
		cursor.execute("CREATE TABLE IF NOT EXISTS Market ( ticker char(20) PRIMARY KEY, prediction varchar(20) )")
		self.conn.commit()

	# This function gets tickerName and predictedClose from Prediction.py 
	# and stores it in the database. 
	def storePrediction(self, tickerName, predictedClose):
		cursor = self.conn.cursor()
		cursor.execute("INSERT INTO Market (ticker, prediction) VALUES (%s, %s);", (tickerName, predictedClose))
		self.conn.commit()

	# Gets ticker from server and searches for data with tickerName=ticker 
	# from server and returns predicted the closing price. 
	def getPredictedClose(self, ticker):
		cursor = self.conn.cursor()
		cursor.execute("SELECT prediction FROM Market WHERE ticker = %s; ", (ticker,))
		data = cursor.fetchone()[0];
		self.conn.commit()
		print("Returned Data: ", data)
		return data

# For testing purpose
def main():
	
	database = DataBase()
	database.createDatabase()
	database.storePrediction("AAPL", "75.55")
	print(database.getPredictedClose("AAPL"))


if __name__ == "__main__": 
    # calling main function 
    main() 