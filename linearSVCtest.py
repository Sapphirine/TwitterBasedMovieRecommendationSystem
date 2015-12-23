##Author Xing Lan
##TPC: Big data analysis
##Linear SVC classification test

#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.svm import LinearSVC
import os
import numpy as np
import pickle
#import time
#import nltk

##set the working dictionary
os.chdir("/Users/lanxing/Desktop/TPC big data/final project/linearSVM")

##read testing data
testdatapos = []
testdataneg = []

text_file = open("test_positive.txt", "r")
lines = text_file.readlines()
for line in lines:
    testdatapos.append(' '.join(line.split()))
text_file.close()

text_file = open("test_negative.txt", "r")
lines = text_file.readlines()
for line in lines:
    testdataneg.append(' '.join(line.split())) 
text_file.close()

##apply the svc model
x_test_pos = np.array([''.join(el) for el in testdatapos[0:len(testdatapos)]])
x_test_neg = np.array([''.join(el) for el in testdataneg[0:len(testdataneg)]])

clf = open('linearSVCclassifier.pickle')
vec = open('vectorizer.pickle')
classifier=pickle.load(clf)
vectorizer=pickle.load(vec)
clf.close()
vec.close()

y_pred_pos=classifier.predict(vectorizer.transform(x_test_pos)).astype(int)
y_pred_neg=classifier.predict(vectorizer.transform(x_test_neg)).astype(int)

print 'Positive correct rate %.2f%%' %(50.0+50.0*y_pred_pos.sum()/y_pred_pos.shape[0]) 
print 'Negative correct rate %.2f%%' %(50.0-50.0*y_pred_neg.sum()/y_pred_neg.shape[0]) 

