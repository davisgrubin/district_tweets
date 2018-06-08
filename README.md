# district_tweets
link to Dash interactive visualization of sentiment polarity time-series: http://ec2-18-222-37-25.us-east-2.compute.amazonaws.com:8050/
code is in sentiment_timeseries.py

#### What can tweets tell us about the partisan make-up of the congressional districts where they are from? 

#### Could they potentially be used alongside poll data to better predict election outcomes?
## How to use this repo
Just clone the repo and run GeoStream.py in a terminal. It will create a stream_tweets folder with each district's tweets & metadata saved in the format <State FIPS #>-<District #>.txt. Once you have collected enough tweets (du -sbh stream_tweets in the bash until its around 9gb to get around how many I had). You can then look at the Partisanship Prediction notebook to see how to read in just the tweets, districts, and parties into a dataframe for reproducing predictions using scikit learn. 


# Collecting Data
## Twitter Streaming API w/ Tweepy
The Twitter Streaming API allows for the collection of tweets by specifiying bounding boxes - in my case I enclosed the continental U.S. 
and then filtered on tweet metadata. While a very small amount of this data has exact geographic coordinates, many do have user specified locations. By creating a index of place names by congressional district using the [relationship](https://www.census.gov/geo/maps-data/data/relationship.html) and [name-lookup](https://www.census.gov/geo/maps-data/data/nlt.html) files made public by census.gov, I was able to create a pipeline that saved tweets originating from accounts with these locations as .txt files with the State FIPS code and district number as a title. Currently I have around 9GB of tweets and corresponding metadata.

# Methods
First I loaded the tweets into a dataframe and did some twitter-specific tokenization and text pre-processing by removing links and english stopwords using Stanford NLP's preprocessing script. 
By treating each district's tweets as a document, I created a TF-IDF matrix and a bag-of-words (as well as SVD for both of them) and used a Multinomial Naive Bayes and SVM  classifier trained using Stochastic Gradient Descent on each for a baseline. The labels were whether that district was represented by a Democrat(0) or a Republican(1).

# Results
For the model evaluation I split the districts and their associated tweets into a training set of 307. Surprisingly the most simple approach, a bag of words with Naive Bayes had a 3 fold cross validated score of 70 % while the Tfidf reduced to 50d using SVD with a SVM as classifier performed at 74% accuracy. I've also incorporated sentiment analysis using VADER analysis on tweets from each district containing the terms "Trump", "clinton", "republican" and "democrat", though these features do not appear to be making much of a difference as of right now. 

# Goals
I'm currently working on how to apply more dense, semantically rich features such as GloVe and word2vec along with neural nets to this "district as document" classification schema. In the future I'd like to change my dependent variable to COOK PVI, a measure of congressional partisanship in each district that is calculated by comparing district-level presidential election results to those of the national presidential election. From there the statistically complex task of trying to augment polling data with this information would begin. I'm also curious to see how far I can get with just using vector representations and ML algorithms without trying any extensive feature engineering.  

If you missed it at the top, I've created a simple interactive visualization using Dash that allows users to search terms and get a time-series of sentiment polarity of tweets containing those terms. The code is in sentiment_timeseries.py and the application is here: http://ec2-18-222-37-25.us-east-2.compute.amazonaws.com:8050/
Keep in mind this uses the free Twitter API and therefore doesn't have very large numbers of tweets for certain terms!







