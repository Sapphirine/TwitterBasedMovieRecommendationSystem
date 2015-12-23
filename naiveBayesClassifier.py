##Author:Xing Lan
##TPC:Big data analysis
##Training Naive Bayes Model

import os
import nltk
import pickle

##set the working dictionary
os.chdir("/Users/lanxing/Desktop/TPC big data/final project/naivebayes")

##readfile
trains = []

text_file = open("positive.txt", "r")
lines = text_file.readlines()
for line in lines:
    line_split=line.split()
    trains.append((line_split,'positive'))  
text_file.close()

text_file = open("negative.txt", "r")
lines = text_file.readlines()
for line in lines:
    line_split=line.split()
    trains.append((line_split,'negative'))  
text_file.close()

##print trains
print 'Reading files completed'

##Classifer
##extract features
def get_words_in_trains(trains):
    all_words = []
    for (words, sentiment) in trains:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

word_features = get_word_features(get_words_in_trains(trains))
##print word_features

def extract_features(document):
    document_words = set(document)    ##Distinct
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

##extract_features(['love', 'this', 'car'])
training_set = nltk.classify.apply_features(extract_features, trains)
##print training_set
print 'Extract features completed'

##training the naive bayes model
classifier = nltk.NaiveBayesClassifier.train(training_set)
##print classifier.show_most_informative_features(32)
print 'Naive bayes model training completed'
#tweet = 'Your song is horrible'
#print classifier.classify(extract_features(tweet.split()))

#save classifier
f = open('naivebayes_classifier.pickle', 'wb')
pickle.dump(classifier, f)
f.close()

f = open('word_features.txt', 'w')
for word in word_features:
    f.write(word)
    f.write(' ')
f.close()

#load classifier
#f = open('naivebayes_classifier.pickle', 'rb')
#classifier = pickle.load(f)
#f.close()
#print 'accuracy:', nltk.classify.util.accuracy(classifier, testfeats)
