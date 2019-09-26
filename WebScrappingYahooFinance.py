import ssl
import json
import os
import ast
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import urllib.error
from urllib.request import Request, urlopen


class WebScrapYahooFinance(object):

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
	def __init__(self, ticker):
		# Yahoo finance URL to get all the details from
		self.url = "http://finance.yahoo.com/quote/%s?p=%s"%(ticker, ticker)

		# Ignoring all the SSL certificate errors
		ctx = ssl.create_default_context()
		ctx.check_hostname = False
		ctx.verify_mode = ssl.CERT_NONE


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
	def parseData(self):
		# Accessing it using as a Mozilla browser
		req = Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
		
		# Get all the source page of the passed url
		webPageSource = urlopen(req).read()

		soup = BeautifulSoup(webPageSource, 'html.parser')
		html = soup.prettify('utf-8')

		# Stores summary of Company Stock Price
		companyStockDetails = {}

		# Stores Previous Close, Open, Fifty_two-WK_range,
		# TD_VOLUME, AVERAGE_VOLUME_3MONTH, MARKET_CAP, PE_RATIO,
		# EPS_RATIO, DIVIDEND_AND_YIELD, EX_DIVIDEND_DATE, 
		# ONE_YEAR_TARGET_PRICE
		priceDetails = {}

		# Extracts PRESENT_VALUE from the html source of given url 
		for span in soup.findAll('span', attrs={'class': 'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'}):
		    companyStockDetails['PRESENT_VALUE'] = span.text.strip()

		# Extracts PRESENT_GROWTH from the html source of given url 
		for div in soup.findAll('div', attrs={'class': 'D(ib) Va(t)'}):
		    for span in div.findAll('span', recursive=False):
		        companyStockDetails['PRESENT_GROWTH'] = span.text.strip()

		# Extracts PREV_CLOSE from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'PREV_CLOSE-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['PREV_CLOSE'] = span.text.strip()
		
		# Extracts OPEN from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'OPEN-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['OPEN'] = span.text.strip()
		
		# Extracts FIFTY_TWO_WK_RANGE from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'FIFTY_TWO_WK_RANGE-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['FIFTY_TWO_WK_RANGE'] = span.text.strip()

		# Extracts TD_VOLUME from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'TD_VOLUME-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['TD_VOLUME'] = span.text.strip()

		# Extracts AVERAGE_VOLUME_3MONTH from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'AVERAGE_VOLUME_3MONTH-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['AVERAGE_VOLUME_3MONTH'] = span.text.strip()
		
		# Extracts MARKET_CAP from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'MARKET_CAP-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['MARKET_CAP'] = span.text.strip()

		# Extracts PE_RATIO from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'PE_RATIO-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['PE_RATIO'] = span.text.strip()

		# Extracts EPS_RATIO from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'EPS_RATIO-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['EPS_RATIO'] = span.text.strip()
		
		# Extracts DIVIDEND_AND_YIELD from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'DIVIDEND_AND_YIELD-value'}):
		    priceDetails['DIVIDEND_AND_YIELD'] = td.text.strip()

		# Extracts EX_DIVIDEND_DATE from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'EX_DIVIDEND_DATE-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['EX_DIVIDEND_DATE'] = span.text.strip()
		
		# Extracts ONE_YEAR_TARGET_PRICE from the html source of given url 
		for td in soup.findAll('td', attrs={'data-test': 'ONE_YEAR_TARGET_PRICE-value'}):
		    for span in td.findAll('span', recursive=False):
		        priceDetails['ONE_YEAR_TARGET_PRICE'] = span.text.strip()

		companyStockDetails['priceDetails'] = priceDetails

		print(companyStockDetails)
		return companyStockDetails

def main():
	webscrap = WebScrapYahooFinance("AAPL")
	webData = webscrap.parseData()
	print(webData)

if __name__ == "__main__": 
    # calling main function 
    main() 