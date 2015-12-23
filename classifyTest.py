##Author Xing Lan
##TPC: Big data analysis
##TestSVM and judge positive or negative
##Movie review without geo tag

import MySQLdb
import sys
import os
import numpy as np
import pickle
import string
import re
import enchant
from nltk.metrics import edit_distance
from enchant.tokenize import get_tokenizer
from nltk import stem

##set the working dictionary
os.chdir("/Users/lanxing/Desktop/TPC big data/final project/linearSVM")

##Read the classifier
if locals().has_key("classifier"):
    print "Classifier has already been read"
else:
    clf = open('linearSVCclassifier.pickle')
    classifier=pickle.load(clf)
    clf.close()

if locals().has_key("vectorizer"):
    print "Vectorizer has already been read"
else:
    vec = open('vectorizer.pickle')
    vectorizer=pickle.load(vec)
    vec.close()
print 'Reading completed'


##Process text
replacement_patterns = [
    (r'won\'t', 'will not'),
    (r'can\'t', 'cannot'),
    (r'i\'m', 'i am'),
    (r'isn\'t', 'is not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would'),]
patterns = [(re.compile(pattern), repl) for (pattern, repl) in replacement_patterns]
def expand(s):
    s = re.sub(r'<br />',' ', s)
    for (pattern, repl) in patterns:
        (s, count) = re.subn(pattern, repl, s)
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    s = regex.sub(' ', s)
    return s
        
repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
repl = r'\1\2\3'
dt = enchant.Dict("en_US")
def repeatreplace(word):
    try:
        if dt.check(word[0]):
            return word[0]
        repl_word = repeat_regexp.sub(repl, word[0])
        if repl_word != word[0]:
            return repeatreplace(repl_word)
        else:
            return repl_word
    except: 
        print word
        return " "

pwl = enchant.request_pwl_dict('stopwordssnowball.txt')
def stopword(word):
    try:
        if not pwl.check(word):
            return word
    except:
        print word
        return ' '        
                        
spell_dict = enchant.Dict("en")
max_dist = 2
def spellreplace(word):
    try:
        if spell_dict.check(word):
            return word
        suggestions = spell_dict.suggest(word)
        if suggestions and edit_distance(word, suggestions[0]) <= max_dist:
            return suggestions[0]
        else:
            return word
    except:
        print word
        return " "
        
snowball = stem.snowball.EnglishStemmer()
def checkstem(word):
    try:    
        word = snowball.stem(word)
        return word
    except:
        print word    
        return " "
                                                                
#Function for preprocessing the text
def common_preprocessing(text):
    words = []
    s=expand(text)
    tknzr = get_tokenizer("en_US")
    for w in tknzr(s):
        w=repeatreplace(w)
        w=spellreplace(w)
        w=w.lower() 
        w=checkstem(w)
        w=stopword(w)
        if w:
            words.append(w)
    text = " ".join(words)
    return text

##Test positive or negative
while(1):
        test_sentence = raw_input("Please enter the test sentence, \nIf you want to exit, enter nothing and press enter button\n")
        if test_sentence=="":
            print("Thanks for your using. Goodbye!")
            break
        else:
            test_sentence = np.array(["".join(common_preprocessing(test_sentence))])
            test_pred=classifier.predict(vectorizer.transform(test_sentence)).astype(int)[0]
            if test_pred==1:
                print('This sentence is positive\n')
            elif test_pred==-1:
                print('This sentence is negative\n')