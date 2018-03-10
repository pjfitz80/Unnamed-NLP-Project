
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import os
 
# Credentials needed to access the API and make requests.
# API key
consumerkey = ''
# API secret
consumersecret = ''
# Access token
accesstoken = ''
# Access token secret
accesstokensecret = ''
 
authorization = OAuthHandler(consumerkey, consumersecret)
authorization.set_access_token(accesstoken, accesstokensecret)
 
class Listener(StreamListener):
    def __init__(self, path=None):
        self.path = path
        self.siesta = 0
        self.nightnight = 0
 
    def on_data(self, data):
        tweet = data.split(',"text":"')[1].split('","source":"')[0]
        print time.strftime("%Y%m%d_%H%M%S"), tweet
 
        # Open, Write then Close the file
        savefile = open(self.path, 'ab')
        savefile.write(data)
        savefile.close()
 
    def on_error(self, status_code):
        print 'Error:', str(status_code)
 
        if status_code == 420:
            sleepy = 60 * math.pow(2, self.siesta)
            print time.strftime("%Y%m%d_%H%M%S")
            print "A reconnection attempt will occur in " + \
            str(sleepy/60) + " minutes."
            print '''
            *******************************************************************
            From Twitter Streaming API Documentation
            420: Rate Limited
            The client has connected too frequently. For example, an 
            endpoint returns this status if:
            - A client makes too many login attempts in a short period 
              of time.
            - Too many copies of an application attempt to authenticate 
              with the same credentials.
            *******************************************************************
            '''
            time.sleep(sleepy)
            self.siesta += 1
        else:
            sleepy = 5 * math.pow(2, self.nightnight)
            print time.strftime("%Y%m%d_%H%M%S")
            print "A reconnection attempt will occur in " + \
            str(sleepy) + " seconds."
            time.sleep(sleepy)
            self.nightnight += 1
        return True        
 
filename = "tweets_collected"
 
script_dir = os.path.dirname(__file__)
rel_path = filename + ".json"
file_path = os.path.join(script_dir, rel_path)
 
twitterStream = Stream(
    authorization, 
    Listener(
        path = file_path
    )
)
#bounding boxes for United States 
 #[[[-127.3268036048,24.7267702114],[-55.7367659292,24.7267702114],[-55.7367659292,49.0784496439],[-127.3268036048,49.0784496439],[-127.3268036048,24.7267702114]]]
twitterStream.filter(locations=[-74.0231,45.3299,-73.3846,45.7311])