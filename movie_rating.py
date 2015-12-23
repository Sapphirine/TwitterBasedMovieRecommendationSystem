##Author Xing Lan
##TPC: Big data analysis
##Linear SVC classification
##Movie review without geo tag

import MySQLdb
import sys
import os
import numpy as np
import pickle
import string
import re
import enchant
import correctSnowball
from nltk.metrics import edit_distance
from enchant.tokenize import get_tokenizer
from nltk import stem


##set the working dictionary
os.chdir("/Users/lanxing/Desktop/TPC big data/final project/linearSVM")

##Read the classifier
clf = open('linearSVCclassifier.pickle')
vec = open('vectorizer.pickle')
classifier=pickle.load(clf)
vectorizer=pickle.load(vec)
clf.close()
vec.close()
print 'Reading file completed'

##define function to process tweet data
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

##connect SQL
try:
    con=MySQLdb.connect(host="",user="",passwd="",db="")
    print 'Connection success'              
except MySQLdb.Error, e:  
    sys.exit(1)
    print 'Connection fail'

##Create array to save the result    
cursor = con.cursor()
sql="SELECT MAX(movieid) FROM tweets"    
cursor.execute(sql)   
maxmovieid = cursor.fetchone()            
maxmovieid = int(maxmovieid[0])

cursor = con.cursor()
sql="SELECT MIN(movieid) FROM tweets"    
cursor.execute(sql)   
minmovieid = cursor.fetchone()            
minmovieid = int(minmovieid[0])                  

cursor = con.cursor()
sql="SELECT MAX(geoid) FROM tweets"    
cursor.execute(sql)   
maxgeoid = cursor.fetchone()            
maxgeoid = int(maxgeoid[0])

cursor = con.cursor()
sql="SELECT MIN(geoid) FROM tweets"    
cursor.execute(sql)   
mingeoid = cursor.fetchone()            
mingeoid = int(mingeoid[0]) 

scores=np.zeros([maxmovieid-minmovieid+1,maxgeoid-mingeoid+1]).astype(float)
tweetnum=np.zeros([maxmovieid-minmovieid+1,maxgeoid-mingeoid+1]).astype(int)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
##select the movieid and number of tweets
thredhold=300
thredhold2=10
cursor = con.cursor()
sql="""SELECT movieid,geoid,COUNT(DISTINCT tweet) AS tweetsnum FROM tweets GROUP BY movieid,geoid ORDER BY geoid,movieid"""   
cursor.execute(sql)   
for row in cursor:
    tweetnum[int(row[0]-1)][int(row[1])]=int(row[2])
##print tweetnum

##score the movie
for i in range(0,tweetnum.shape[0]):
##score the data with geoid=0
    if tweetnum[i][0]<thredhold:
        scores[i][0]=0
        print "movie %d geoid=0 do not have enough tweets" %(i+1)
    else:
        try:
            id=i+1
            cursor = con.cursor()
            sql="""SELECT DISTINCT tweet FROM tweets WHERE movieid = %d AND geoid = 0 ORDER BY date DESC LIMIT %d """ %(id,thredhold)    
            cursor.execute(sql)   
            tweets = np.array(["".join(common_preprocessing(row[0])) for row in cursor]) 
            tweets_pred=classifier.predict(vectorizer.transform(tweets)).astype(int)
            score= (5.0+5.0*tweets_pred.sum()/tweets_pred.shape[0]) 
            scores[i][0]=score
        except:
            print "movie %d geoid=0 training failed" %(id)
##score the data with geoid!=0    
    for j in range(1,tweetnum.shape[1]):
        if tweetnum[i][j]<thredhold2:
            scores[i][j]=0
            print "movie %d geoid=%d do not have enough tweets with geotag" %(i+1,j)
        else:
            try:
                id=i+1
                cursor = con.cursor()
                sql="""SELECT DISTINCT tweet FROM tweets WHERE movieid = %d AND geoid = %d """ %(id,j)    
                cursor.execute(sql)   
                tweets = np.array(["".join(common_preprocessing(row[0])) for row in cursor]) 
                tweets_pred=classifier.predict(vectorizer.transform(tweets)).astype(int)
                score= (5.0+5.0*tweets_pred.sum()/tweets_pred.shape[0]) 
                scores[i][j]=score
            except:
                print "movie %d geoid=%d training failed" %(id,j)
    
##print tweets_pred.sum()
##print scores
print 'movieid\t',
for i in range(0,scores.shape[1]):
    print 'scoregeoid=%d\t'%(i),
print ''
for i in range(0,scores.shape[0]):
    print '%d\t'%(i+1),
    for j in range(0,scores.shape[1]):
        print '%.2f\t\t'%(scores[i][j]),
    print ''

##Cut off the connection
if con:    
    con.close()
