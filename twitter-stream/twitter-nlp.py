from nltk.twitter import Query, Streamer, Twitter, TweetViewer, TweetWriter, credsfromfile
from nltk.corpus import twitter_samples
#retrieving twitter data and interfacing with API
oauth = credsfromfile()
#tw = Twitter()
#tw.tweets(to_screen=False, limit=25)


#sample public twitter stream
#client = Streamer(**oauth)
#client.register(TweetViewer(limit=10))
#client.sample()

#client = Query(**oauth)
#tweets = client.search_tweets(keywords='nltk', limit = 50)
#tweet = next(tweets)
#from pprint import pprint
#pprint(tweet, depth = 1)

print twitter_samples.fileids()

strings = twitter_samples.strings('tweets.20150430-223406.json')
for string in strings[:15]:
    print(string)


