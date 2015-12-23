##Author Xing Lan
##TPC: Big data analysis
##Linear SVC classification

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
import os
import numpy as np
import pickle
import time
import nltk


##set the working dictionary
os.chdir("/Users/lanxing/Desktop/TPC big data/final project/linearSVM")

##read training data
traindata = []
trainlabel = []

text_file = open("positive.txt", "r")
lines = text_file.readlines()
for line in lines:
    traindata.append(' '.join(line.split()))
    trainlabel.append('1')  
text_file.close()

text_file = open("negative.txt", "r")
lines = text_file.readlines()
for line in lines:
    traindata.append(' '.join(line.split()))
    trainlabel.append('-1')  
text_file.close()

#Converting the train data into array format for scikit-learn operation
x_train = np.array([''.join(el) for el in traindata[0:len(traindata)]])
y_train = np.array([el for el in trainlabel[0:len(trainlabel)]])

#Defining a vectorizer for feature extraction
#vectorizer = CountVectorizer(min_df=1,ngram_range=(1, 3))
vectorizer = TfidfVectorizer(ngram_range=(1,3), use_idf=True, analyzer='word', lowercase=True, encoding='utf-8', min_df=3)#, max_df=1995)

#Extracting features from train data
x_train_vector = vectorizer.fit_transform(x_train)

#Defing a classifier for classification
classifier = LinearSVC(C=0.5).fit(x_train_vector, y_train)
clf = open('linearSVCclassifier.pickle', 'wb')
vec = open('vectorizer.pickle','wb')
pickle.dump(classifier, clf)
pickle.dump(vectorizer,vec)
clf.close()
vec.close()

print 'Training Done'

