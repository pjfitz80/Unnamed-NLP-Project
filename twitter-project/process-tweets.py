# -*- coding: utf-8 -*-
#process stored tweets from Twitter Public Stream
import os
import re
import json
import string
import pandas as pd
import matplotlib.pyplot as plt
#from nltk.twitter.util import json2csv
from nltk.tokenize import TweetTokenizer

data_files = ["raw_data/output.txt", "raw_data/output2.txt", "raw_data/output3.txt", "raw_data/output4.txt", "raw_data/output5.txt", 
              "raw_data/output6.txt", "raw_data/output7.txt", "raw_data/output8.txt", "raw_data/output9.txt", "raw_data/output10.txt",
              "raw_data/output11.txt", "raw_data/output12.txt", "raw_data/output13.txt", "raw_data/output14.txt", "raw_data/output15.txt"]
raw_data = []
processed_tweets = []
tknzr = TweetTokenizer()


#for file in files:
    
def readTweetsFromFiles():   
    #get tweet, date, category (text, created_at, category)
    tweetCount = 0
    script_dir = os.path.dirname(__file__)
    for file in data_files:
        #process 50k tweets at a time
        tweets_json = open(os.path.join(script_dir, file), "r")
        for line in tweets_json:
            if(tweetCount % 1000 == 0):
                print "number of tweets read in: " + str(tweetCount)
            try:
                tweet = json.loads(line)
                raw_data.append((tweet['created_at'], tweet['text']))
                tweetCount += 1
            except:
                continue
    print "number of tweets read in: " + str(len(raw_data))
    
    #load stopwords
    stopwords = []
    script_dir = os.path.dirname(__file__)
    rel_path = "corpora/stopwords.txt"
    file_path = os.path.join(script_dir, rel_path)
    sw_file = open(file_path, 'r')
    words = sw_file.readlines()
    for w in words:
        sw = w.strip()
        stopwords.append(sw)

    for tweet in raw_data:
        processed_tweets.append(processTweet(tweet, stopwords))
    for p in processed_tweets:
        print p
    

def processTweet(tweet, stopwords):
    #clean up data from Twitter and categorize
    categories= [{["@apple", "#apple", "@tim_cook"]: "apple"},
                 {["@microsoft", "microsoft", "@satyanadella"] : "microsoft"},
                 {["@google", "#google", "@sundarpichai"] : "google"}]
    tweetCategory = 'unknown'
    tweetDate = tweet[0]
    tweetText = tweet[1]
    tweetText = re.sub(r'((http?://[^\s]+))','URL',tweetText)
    
    parseText = tknzr.tokenize(tweetText)
    for t in parseText:
        if t in stopwords:
            parseText[:] = [x for x in parseText if x != t] 
        for c in categories:
            for term in c.keys():
                if t == term:
                    tweetCategory = categories[c]
    tweetText = "".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in parseText]).strip()
    return ((tweetDate, tweetText, tweetCategory))

def main():
    readTweetsFromFiles()

    
if __name__=="__main__":
    main()
    
    
    
