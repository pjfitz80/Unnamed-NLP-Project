# -*- coding: utf-8 -*-
#process stored tweets from Twitter Public Stream
import json
import pandas as pd
import matplotlib.pyplot as plt

tweets_data = []

#files1 = 'twitter_data.txt'
#files2 = 'twitter_data1.txt'
files3 = 'twitter_data2.txt'

#for file in files:
    
         
tweetCount = 0
tweets_file1 = open(files3, "r")

for line in tweets_file1:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
#for line in tweets_file2:
#    try:
#        tweet = json.loads(line)
#        tweets_data.append(tweet)
#    except:
#        continue
#for line in tweets_file2:
#    try:
#        tweet = json.loads(line)
#        tweets_data.append(tweet)
#    except:
#        continue
print len(tweets_data)
