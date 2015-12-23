Description for codes below:

* twitter API credential, Database credentials are removed from the original code. user needs to get his/her own twitter API key, database setup for the code to work. 

* training and testing data for Sentiment analysis model is in the "training and testing data after processing" foler

tweetextraction.py			python code to extract tweets from twitter and store in database.(input from source.txt to search for related movie keywords)

linearSVM.py      			Training the Linear SVC model
linearSVCtest.py 			Calculate the correct rate of SVC models
movie_rating.py				Calculate the rating in different area
movie_rating_by_date.py			Calculate the rating every day
classifyTest.py				Input a sentence and classify its sentiment
naiveBayesClassifier.py			Training the naive bayes classifier
crossvalid.py				Calculate the correct rate of naive bayes classifier


stopwordssnowball.txt			Stop words dictionary
source.txt				movie search keywords for tweet extraction (for each row, first item is keyword, 2nd item is movieid)


