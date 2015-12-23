##Author:Xing Lan
##TPC:Big data analysis
##Load naive bayes model

import os
import nltk
import pickle

##set the working dictionary
os.chdir("/Users/lanxing/Desktop/TPC big data/final project/naivebayes")


#load classifier
f = open('naivebayes_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

word_features = []

text_file = open("word_features.txt", "r")
words = text_file.readline()
word_features=words.split() 
text_file.close()

#Read test file
testfeats = []
text_file = open("test_positive.txt", "r")
lines = text_file.readlines()
for line in lines:
    line_split=line.split()
    testfeats.append((line_split))  
text_file.close()

def extract_features(document):
    document_words = set(document)    ##Distinct
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features
    
cor=0
for row in testfeats:
    if classifier.classify(extract_features(row))=="positive":
        cor=cor+1
#        print cor,
#print ''        
print 'Positive correct rate %.2f%%' %(float(cor)/len(testfeats)*100) 

##Negative data set
testfeats = []
text_file = open("test_negative.txt", "r")
lines = text_file.readlines()
for line in lines:
    line_split=line.split()
    testfeats.append((line_split))  
text_file.close()
     
cor=0
for row in testfeats:
    if classifier.classify(extract_features(row))=="negative":
        cor=cor+1
#       print cor,
#print ''         
print 'Negative correct rate %.2f%%' %(float(cor)/len(testfeats)*100)          