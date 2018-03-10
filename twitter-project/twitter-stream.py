# -*- coding: utf-8 -*-
#file for retrieving and storing Twitter streaming data
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "79774611-WHiAr4n314kyjpXiHXrAfA64TF88rv0OKbyIwgWOQ"
access_token_secret = "XUl8KAlpUXL1OpNxCtczihQLiYfXSuFcAisxFukF8eQok"
consumer_key = "bRW8PGbY3KUgkjuAJopSeGYZd"
consumer_secret = "CHKMI1YOzhDULbMZyVE4edLl2n9jb9E6LK8argFr4P2noQU91R"


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['#apple', '#microsoft', '#google', '@apple', '@microsoft', '@google', '@sundarpichai', '@satyanadella', '@tim_cook'], languages=['en'])
    #stream.filter(track=['apple, microsoft, google'], languages=['en'])


