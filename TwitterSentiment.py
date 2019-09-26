import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob 

class TwitterClient(object):

	"""
	def __init__():

	NAME

	        def __init__(): - Initiliaze Twitter Client
	SYNOPSIS

	        def __init__(self)

	            self: Represents the instance of the class

	DESCRIPTION

	        This is a constructor for the class TwitterClient. It initializes count
	        of postive, negative and neutral tweets. It also stores consumer_key,
	        consumer_secret, acces_token and access_token_secret which are used
	        while getting access to Tweeter API using tweepy. Handles authentication
	        to the API, if api can not be accessed, then a error message is show

	        The API instance will be set to the class which can be later used to 
	        get tweets from twitter

	RETURNS

	        Returns nothing, initializes all the variable which are used in other 
	        member functions

	AUTHOR

	        Anuj Bastola

	DATE

	        09:28 PM 08/28/2019

	"""
	def __init__(self):

		# Counts positive, neutral and negative number of tweets
		self.positive = 0
		self.neutral = 0
		self.negative = 0

		# Consumer API Keys, Access Tokens & access token secret
		consumer_key = "ni4wOGxUP3OLi9NhtC4GLn2aV" 
		consumer_secret = "RLsuqdKpbTWhgHPXDicFOmq70DV7DQF5AspnCOZaGZzsMShaY1"
		access_token = "826845349516103687-QsCyrBhn839GBAx3tWkLgb8t4WBCojp"
		access_token_secret = "IFEIDvDFTgakYDv0RNLnPlv48jlgVPJJL83tJ9mw46q9e"

		try:
			# Authentication Handler by passing consumer_key & consumer_secret
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# Set Twitter Access token in order to use the twitter services
			self.auth.set_access_token(access_token, access_token_secret)
			# API Context for using the tweepy functionality
			self.api = tweepy.API(self.auth)
		except Exception as e:
			print("Authentication to Twitter Application Failed, Error: ", e)
			raise
		else:
			pass
		finally:
			pass

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
	# Regular expression to clean tweets
	def cleanTweets(self, tweet):
		# removing all the URLS
		tweet = re.sub('http\S+\s*', '', tweet)
		# remove RT and cc
		tweet = re.sub('RT|cc', '', tweet)
		# remove hashtags
		tweet = re.sub('#\S+', '', tweet)
		# remove mentions
		tweet = re.sub('@\S+', '', tweet)
		# remove punctuations
		tweet = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), '', tweet)
		# remove extra whitespace
		tweet = re.sub('\s+', ' ', tweet)
		# Removes all the emoji
		return tweet.encode('ascii', 'ignore').decode('ascii')


	"""
	def getTweetSentiment():

	NAME
			
			def getTweetSentiment(): Gets sentiment score of a tweet
	SYNOPSIS

	        def getTweetSentiment(self, tweet)

	            self: Represents the instance of the class
	            tweet: Cleaned Tweet after applying regular expressions which 
	            are extracted from Twitter 

	DESCRIPTION

	        This is a function initializes instance from TextBlob library. 
			When TextBlob function is passed, it does Sentiment Analyis of 
			the tweet and return result to 'sentimentAnalysis'. The result 
			of the library stores polarity of the tweet. If polarity is
			greater than 0, the tweet is positive. If polarity is equal to 
			0, then the tweet is neutral, else if polarity is less than 0, 
			then the tweet is negative

			Increases respective count of postive, negative or neutral based 
			on the response from TextBlob

	RETURNS

	        Does not return anything, increases the count

	AUTHOR

	        Anuj Bastola

	DATE

	        11:37 PM 08/28/2019

	"""
	def getTweetSentiment(self, tweet):
		# Gets the sentiment Analysis of each tweet
		sentimentAnalysis = TextBlob(tweet)

		# Checks whether the tweet is negative, positive or neutral
		if sentimentAnalysis.sentiment.polarity > 0:
			# Increase positive tweet number if the polarity is greater than 0
			self.positive = self.positive + 1
		elif sentimentAnalysis.sentiment.polarity == 0:
			# Increase neutral tweet number if the polarity is equal to 0
			self.neutral = self.neutral + 1
		else:
			# Increase negative tweet number if the polarity is less than 0
			self.negative = self.negative + 1


	"""
	def getTweets():

	NAME
			
			def getTweets(): Gets tweets and information about all the 
								tweets by analyzing the Sentiment 
	SYNOPSIS

	        def getTweets(self, companyName, tweetsNum)

	            self: Represents the instance of the class
	            companyName: Name of the company whose tweets will be extracted
	            			 from twitter
	            tweetsNum: Number of tweets to be extracted from Twitter which 
	            			mentions the companyName

	DESCRIPTION

	        This is a function calls api.search of tweepy and gets all the 
	        information of tweets. for every tweet in fetched_tweets, it applies 
	        cleanTweets function and gets the sentiment for each tweet.
	        It stores all the tweets in a dictionary 'dataToSend'. 'dataToSend'
	        also stores the total number of positive, negative and neutral 
	        tweets

	RETURNS

	        Returns a dictionary that contains tweets, number of positive, negative
	        and neutral tweets

	AUTHOR

	        Anuj Bastola

	DATE

	        01:17 PM 08/29/2019

	"""
	# Function that retrieves tweets related to the 'companyName'
	def getTweets(self, companyName, tweetsNum):
		tweets = []

		try:
			# Calling tweepy api to get all the tweets that mentions a particular company
			fetched_tweets = self.api.search(q=companyName, count=tweetsNum, lang='en')

			#parsing each tweets
			for tweet in fetched_tweets:
				parsed_tweet = {}
				# Gets pure text from tweet after filtering out unnecsary characters and emojis
				pureTweet = (self.cleanTweets(tweet.text)).strip()
				# Calculates sentiment of pureTweet and increase count of positive, negative or neutral
				self.getTweetSentiment(pureTweet)
				# parsed_tweet['text'] = self.cleanTweets(pureTweet.strip())
				
				if tweet.retweet_count > 0:
					if tweet.text not in tweets:
						tweets.append(tweet.text)
				else:
					tweets.append(tweet.text)

			dataToSend = {}
			# Stores all information of tweet(tweet, sentiment analysis result) to send back to mobile application
			dataToSend['Tweets'] = tweets
			dataToSend['Positive'] = self.positive
			dataToSend['Negative'] = self.negative
			dataToSend['Neutral'] = self.neutral

			return dataToSend

		except Exception as e:
			raise e

# For Testing purpose
def main():
	api = TwitterClient()
	tweetDetails = api.getTweets(companyName="Tesla", tweetsNum=200)
	print(tweetDetails)

if __name__ == "__main__": 
    # calling main function 
    main() 