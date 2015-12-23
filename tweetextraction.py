from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy import AppAuthHandler
from tweepy import Cursor
from pymysql import Error
import pymysql
import re
import time

def insert(cur,data):
    """Insert a record"""
    sql = "INSERT INTO tweets VALUES ('%s','%s','%s','%s')" %(data[0],data[1],data[2],data[3])
    try:
        # print ("%s,%s",(sql, params))
        cur.execute(sql)
        conn.commit() # pymysql does not autocommit
    except pymysql.Error as e:
        print("sth wrong when writing to db")

def process_tweet(text):
    for (pattern, repl) in patterns: 
        text = re.sub(pattern, repl, text)
    text = re.sub(r'[^\w\s]',' ',text)
    return text


#consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

auth = AppAuthHandler(ckey, csecret)
api = API(auth)

conn = pymysql.connect(db='', host='', port=3306,user='',passwd='',use_unicode=True, charset='utf8')
cur = conn.cursor()

with open("source.txt", "r") as f:
    movies = f.read().replace('\t', '\n').split('\n')
searchterms = dict(zip(movies[::2], movies[1::2]))
geo=["40.63063,-77.695312,1500km","34.646766,-90.703125,1500km","44.754383,-96.246414,1500km","37.517181,-110.675583,1500km","46.910875,-117.553711,1500km"]

replacement_patterns = [   (r'won\'t', 'will not'), (r'can\'t', 'cannot'), (r'i\'m', 'i am'), (r'isn\'t', 'is not'),
    (r'(\w+)\'ll', '\g<1> will'), (r'(\w+)n\'t', '\g<1> not'), (r'(\w+)\'ve', '\g<1> have'), (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would'),(r'https:\S*',' '),(r'@\S*',' '),(r'#\S*',' '),(r'rt\S*',' ')]
patterns = [(re.compile(pattern), repl) for (pattern, repl) in replacement_patterns]

for eachsearch in searchterms:
    print(eachsearch)
    for tweet in Cursor(api.search, q=eachsearch,lang="en",count=100).pages(30):
        for subtweet in tweet:
            try:    
                content=subtweet.text.lower()
                content=content.replace(eachsearch.lower(),'')
                content=process_tweet(content)
                timeline=subtweet.created_at
                timeline=str(timeline).split(' ')[0]
                month = timeline.split('-')[1]
                day = timeline.split('-')[2]
                if int(day)>17:
                    data=[searchterms[eachsearch],'0',content,timeline]
                    insert(cur,data)
            except Error as e:
                print(e)

    for i in range(1,6):
        for tweet in Cursor(api.search, q=eachsearch,lang="en", geocode=geo[i-1],count=100).pages(30):
            for subtweet in tweet:
                try:    
                    content = subtweet.text.lower()
                    content = content.replace(eachsearch.lower(),'')
                    content = process_tweet(content)
                    timeline=subtweet.created_at
                    timeline=str(timeline).split(' ')[0]
                    month = timeline.split('-')[1]
                    day = timeline.split('-')[2]
                    if int(day)>14:
                        data=[searchterms[eachsearch],str(i),content,timeline]
                        insert(cur,data)
                except Error as e:
                    print(e)

cur.close()
conn.close()







