import pandas as pd
import bs4 as bs
import urllib.request
import time

class ScrapStockHistory(object):

	def __init__(self):
		pass


	def get_ticker(self, ticker, day_one, day_two):

	    url = 'https://finance.yahoo.com/quote/' + ticker + '/history?period1=' + day_one + '&period2=' + day_two + '&interval=1d&filter=history&frequency=1d'
	    source = urllib.request.urlopen(url).read()
	    soup =bs.BeautifulSoup(source,'lxml')
	    tr = soup.find_all('tr')
	    data = []
	    for table in tr:
	    	td = table.find_all('td')
	    	row = [i.text for i in td]
	    	data.append(row)        
	      
	    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
	    data = data[1:-2]
	    df = pd.DataFrame(data)
	    df.columns = columns
	    df.set_index(columns[0], inplace=True)
	    # df = df.convert_objects(convert_numeric=True)
	    df = df.iloc[::-1]
	    df.dropna(inplace=True)
	    return df

def main():
	# April 3, 2018 = 1522728000  (seconds since UNIX epoch in 1970)
	# June 12, 2018 = 1528776000
	# https://finance.yahoo.com/quote/AAPL/history?period1=1522728000&period2=1528776000&interval=1d&filter=history&frequency=1d
	format_string='%Y-%m-%d %H:%M:%S'
	 
	# One day (86400 second) adjustment required to get dates printed to match web site manual output
	date1='2019-08-23 00:00:00'
	date1_epoch = str(int(time.mktime(time.strptime(date1,format_string)))- 86400)
	print("")
	print(date1, date1_epoch)
	 
	date2='2018-09-23 00:00:00'
	date2_epoch = str(int(time.mktime(time.strptime(date2,format_string))))
	print(date2, date2_epoch)
	
	ScrapStock = ScrapStockHistory();
	df = ScrapStock.get_ticker('AAPL', date1_epoch, date2_epoch)
	print(df)

if __name__ == "__main__": 
    # calling main function 
    main() 

