# -*- coding: utf-8 -*-
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

word_features = []    

def main():
    features = load_features()
    
    train_set = features[9500:]
    test_set = features[:1406]
        
    test = processTweet("Just started using @zoho email client on #ios and must admit that it's much better than @gmail from @Google.Better #UI, #UX and faster sync")
    test2 = processTweet("What the hell, @firefox and @Apple? Implement damn date\/time inputs. Chrome has supported for 5 years, Opera for 8.\u2026 https:\/\/t.co\/ZiyAQH8sBt")
    test3 = processTweet("Lovely @google celebration of Iraqi architect Zaha Hadid today https:\/\/t.co\/FrsJUt3RF5 via @\/google.com\/doodles")
    test4 = processTweet("#Apple pay usage peaked in March 2015. Adoption rate is declining. One of the major concerns: security (despite Apple Pay being very secure)")
    
    global word_features
    word_features = get_word_features(get_words_in_tweets(train_set))
    training_set = nltk.classify.apply_features(extract_features, train_set)
    classifier = SklearnClassifier(MultinomialNB())
    classifier.train(training_set)
    #print classifier.show_most_informative_features(40)
    print classifier.classify(extract_features(test))
    print classifier.classify(extract_features(test2))
    print classifier.classify(extract_features(test3))
    print classifier.classify(extract_features(test4))
    testing_set = nltk.classify.apply_features(extract_features, test_set)
    print("MNB_classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)

    


    
    
    
    #vocabulary = set(chain(*[word_tokenize(i[0].lower()) for i in features]))
    #feature_set = [({i:(i in word_tokenize(sentence.lower())) for i in vocabulary}, tag) for sentence, tag in features]

#==============================================================================
#     training_set = nltk.classify.util.apply_features(extract_features, train_set)
#     testing_set = nltk.classify.util.apply_features(extract_features, test_set)
#     print "Training classifier"
#     NB_Classifier = nltk.NaiveBayesClassifier.train(training_set)
#     save_classifier = open("NBClassifer.pickle","wb")
#     pickle.dump(NB_Classifier, save_classifier)
#     save_classifier.close()
#     print("Original Naive Bayes Algo accuracy percent:",(nltk.classify.accuracy(NB_Classifier, testing_set))*100)
#     print NB_Classifier.show_most_informative_features(20)
#     print NB_Classifier.classify(extract_features(test))
#     print NB_Classifier.classify(extract_features(test2))
#     print NB_Classifier.classify(extract_features(test3))
#     print NB_Classifier.classify(extract_features(test4))
#     
#==============================================================================
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

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features
    
def load_features():
    #load training sets and associated features
    script_dir = os.path.dirname(__file__)
    rel_path = "corpora/training.1600000.processed.noemoticon.csv"
    file_path = os.path.join(script_dir, rel_path)
    stanford = loadStanford(file_path, 5000)
    rel_path = "corpora/sanders-corpus.csv"
    file_path = os.path.join(script_dir, rel_path)
    sanders = loadSanders(file_path)
    features = list(itertools.chain(stanford, sanders))
    #features = list(sanders)
    random.shuffle(features)    
    print "Number of features loaded: " + str(len(features))
    #build vocabulary list
    return features


    
def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
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
        if t in ['URL', 'HASHTAG', 'USER']:
            continue
        else:
            features.append(t.lower())
    return features
    
    
if __name__=="__main__":
    main()
    
    


