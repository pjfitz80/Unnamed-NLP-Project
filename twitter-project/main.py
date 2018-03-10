# -*- coding: utf-8 -*-
import os
import nltk
import pickle
import itertools
import re
import random

from training_preprocessing import loadStanford, loadSanders
from nltk.twitter import TweetViewer
from nltk.tokenize import word_tokenize, TweetTokenizer
from itertools import chain
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

feature_list = []

def main():
    f = open('NBClassifer.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    features = load_features()
    
    test_set = features[:1906]
    testing_set = nltk.classify.util.apply_features(extract_features, test_set)
    print("Original Naive Bayes Algo accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)
    print classifier.show_most_informative_features(20)
    
    

def train():
    features = load_features()
    
    train_set = features[39000:]
    test_set = features[:1906]
        
    test ="Just started using @zoho email client on #ios and must admit that it's much better than @gmail from @Google.Better #UI, #UX and faster sync"
    test2 = "What the hell, @firefox and @Apple? Implement damn date\/time inputs. Chrome has supported for 5 years, Opera for 8.\u2026 https:\/\/t.co\/ZiyAQH8sBt"
    test3 = "Lovely @google celebration of Iraqi architect Zaha Hadid today https:\/\/t.co\/FrsJUt3RF5 via @\/google.com\/doodles"
    test4 = "#Apple pay usage peaked in March 2015. Adoption rate is declining. One of the major concerns: security (despite Apple Pay being very secure)"
    test = processTweet(test)
    
    #vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in features]))
    #feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary}, tag) for sentence, tag in features]

    training_set = nltk.classify.util.apply_features(extract_features, train_set)
    testing_set = nltk.classify.util.apply_features(extract_features, test_set)
    print "Training classifier"
    NB_Classifier = nltk.NaiveBayesClassifier.train(training_set)
    save_classifier = open("NBClassifer.pickle","wb")
    pickle.dump(NB_Classifier, save_classifier)
    save_classifier.close()
    print("Original Naive Bayes Algo accuracy percent:",(nltk.classify.accuracy(NB_Classifier, testing_set))*100)
    print NB_Classifier.show_most_informative_features(20)
    print NB_Classifier.classify(extract_features(test))
    print NB_Classifier.classify(extract_features(test2))
    print NB_Classifier.classify(extract_features(test3))
    print NB_Classifier.classify(extract_features(test4))
    
    #MNB_classifier = SklearnClassifier(MultinomialNB())
    #MNB_classifier.train(training_set)
    #print("MNB_classifier accuracy percent:",(nltk.classify.accuracy(MNB_classifier, testing_set))*100)

    #save_classifier = open("MNB_classifier5k.pickle","wb")
    #pickle.dump(MNB_classifier, save_classifier)
    #save_classifier.close()
    
    #BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
    #BernoulliNB_classifier.train(training_set)
    #print("BernoulliNB_classifier accuracy percent:",(nltk.classify.accuracy(BernoulliNB_classifier,testing_set))*100)

    #save_classifier = open("BernoulliNB_classifier5k.pickle","wb")
    #pickle.dump(BernoulliNB_classifier, save_classifier)
    #save_classifier.close()
    
def load_features():
    #load training sets and associated features
    script_dir = os.path.dirname(__file__)
    rel_path = "corpora/training.1600000.processed.noemoticon.csv"
    file_path = os.path.join(script_dir, rel_path)
    stanford = loadStanford(file_path, 20000)
    rel_path = "corpora/sanders-corpus.csv"
    file_path = os.path.join(script_dir, rel_path)
    sanders = loadSanders(file_path)
    features = list(itertools.chain(stanford, sanders))
    #features = list(sanders)
    random.shuffle(features)    
    print len(features)
    #build vocabulary list
    vocabulary = []
    for row in features:
        #print row[0]
        for w in row[0]:
            vocabulary.append(w.lower())
    global feature_list
    feature_list=list(set(vocabulary))
    return features
    
def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in feature_list:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

def processTweet(tweet):
    features = []
    tknzr = TweetTokenizer()
    stopwords = []
    script_dir = os.path.dirname(__file__)
    rel_path = "corpora/stopwords.txt"
    file_path = os.path.join(script_dir, rel_path)
    sw_file = open(file_path, 'r')
    words = sw_file.readlines()
    #remove stopwords and get features
    for w in words:
        sw = w.strip()
        stopwords.append(sw)

    tweet = re.sub(r'((http?://[^\s]+))','URL',tweet)
    tweet = re.sub(r'#([^\s]+)', 'HASHTAG', tweet)
    tweet = re.sub(r'@([^\s]+)', 'USER', tweet)
    tweet = tweet.strip('\'"')
    #bypass for non-unicode chars in stanford corpus
    tweet = tknzr.tokenize(tweet)
    for t in tweet:
        if t in stopwords:
            continue
        else:
            features.append(t.lower())
    return features
    
    
if __name__=="__main__":
    main()
    
    
