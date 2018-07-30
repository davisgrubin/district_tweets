# Examining the Twitterverse of Democratic and Republican Congressional Districts

![screenshot from 2018-07-30 13-52-20](https://user-images.githubusercontent.com/25091693/43414188-110ba3b2-9400-11e8-849c-8bcdb5679ab9.png)
Visualization of Word2Vec embeddings trained on 11,000,000 democratic and 9,000,000 republican tweets. (just democratic are seen above
## Tensorboard visualization of tweets from all Democratic and Republican districts.
These two tensorboard visualizations of word2vec models trained on democratic and republican tweets allow you to see diffrences and simliarities in twitter discourse. Simply pick a topic, user, or term in the search bar and narrow it down to however many nearest neighbors you'd like. The closer words are to eachother, the more semantic context they share in their use.<br/>
Link to democratic dists tensorboard: http://ec2-18-222-37-25.us-east-2.compute.amazonaws.com:8080/#projector&run=.<br/>
Link to republican dists tensorboard: http://ec2-18-222-37-25.us-east-2.compute.amazonaws.com:8090/#projector&run=.


Here is an example of using the T-SNE option to compare clusters of the 100 nearest neighbors of the term 'politics' for both democratic and republican districts.
#### Republican districts 'politics' clusters
![screenshot from 2018-07-30 13-18-29](https://user-images.githubusercontent.com/25091693/43412407-1d244fdc-93fb-11e8-8c82-b6c166592de9.png)

#### Democratic districts 'politics' clusters
![screenshot from 2018-07-30 13-18-13](https://user-images.githubusercontent.com/25091693/43412408-1ea7b948-93fb-11e8-8279-841380609cdf.png)



You can also project along an 'axis' using terms within the corpus - i.e. 'good to bad' or 'harm to care'. Feel free to get creative!
#### Republican districts 'politics' nearest neighbors good to bad:
![rep_goodtobad](https://user-images.githubusercontent.com/25091693/43413266-9bd87a22-93fd-11e8-8278-84f143f34dab.png)

#### Democratic districts 'politics' nearest neighbors good to bad:
![dem_goodtobad](https://user-images.githubusercontent.com/25091693/43413450-179f00d6-93fe-11e8-9aa0-d19b23fdd499.png)

While you're here also check out:
A Dash app that allows you to track the sentiment polarity (positive vs. negative) of all tweets that contain your search term over time. There also options to filter on congressional districts at the individual and party level. The corresponding code is in sentiment_timeseries.py. Click the plot_studio option to get fancy in the toolbar to get fancy.
#### Dash interactive visualization of sentiment polarity time-series: http://ec2-18-222-37-25.us-east-2.compute.amazonaws.com:8050/
![senitment_timeseries](https://user-images.githubusercontent.com/25091693/43411810-49cdc574-93f9-11e8-932d-038a958ba91d.png)
 


Below is my original Galvanize Data Science Capstone and how I started collected tweets filtered by congressional district.
#### Can tweets be used to predict the partisanship of congressional districts?  

## How to use this repo
*I've updated the method I used for my capstone with a new Tweepy Stream Listener that puts the tweets directly into a Postgresql database(Stream_2_Postgres.py), along with other improvements. I'm keeping the description of the original method below and the original file (GeoStream.py) just to showcase how I used it for my capstone. 

Just clone the repo and run GeoStream.py in a terminal. It will create a stream_tweets folder with each district's tweets & metadata saved in the format <State FIPS #>-<District #>.txt. Once you have collected enough tweets (du -sbh stream_tweets in the bash until its around 9gb to get around how many I had). You can then look at the Partisanship Prediction notebook to see how to read in just the tweets, districts, and parties into a dataframe for reproducing predictions using scikit learn. 


# Collecting Data
## Twitter Streaming API w/ Tweepy
The Twitter Streaming API allows for the collection of tweets by specifiying bounding boxes - in my case I enclosed the continental U.S. 
and then filtered on tweet metadata. While a very small amount of this data has exact geographic coordinates, many do have user specified locations. By creating a index of place names by congressional district using the [relationship](https://www.census.gov/geo/maps-data/data/relationship.html) and [name-lookup](https://www.census.gov/geo/maps-data/data/nlt.html) files made public by census.gov, I was able to create a pipeline that saved tweets originating from accounts with these locations as .txt files with the State FIPS code and district number as a title. Currently I have around 9GB of tweets and corresponding metadata.

# Methods
First I loaded the tweets into a dataframe and did some twitter-specific tokenization and text pre-processing by removing links and english stopwords using Stanford NLP's preprocessing script. 
By treating each district's tweets as a document, I created a TF-IDF matrix and a bag-of-words (as well as SVD for both of them) and used a Multinomial Naive Bayes and SVM  classifier trained using Stochastic Gradient Descent on each for a baseline. The labels were whether that district was represented by a Democrat(0) or a Republican(1).

# Results
For the model evaluation I split the districts and their associated tweets into a training set of 307. Surprisingly the most simple approach, a bag of words with Naive Bayes had a 3 fold cross validated score of 70 % while the Tfidf reduced to 50d using SVD with a SVM as classifier performed at 74% accuracy.  

# Goals
I'm currently working on how to apply more dense, semantically rich features such as GloVe and word2vec along with neural nets to this "district as document" classification schema. In the future I'd like to change my dependent variable to COOK PVI, a measure of congressional partisanship in each district that is calculated by comparing district-level presidential election results to those of the national presidential election. I'm curious to see how far I can get with just using vector representations without trying any extensive feature engineering. I may also use tensorboard or t-SNE to create visualizations of republican and democratic word vectors side by side for comparison. 

If you missed it at the top, I've created a simple interactive visualization using Dash that allows users to search terms and get a time-series of sentiment polarity of tweets containing those terms. The code is in sentiment_timeseries.py and the application is here: http://ec2-18-222-37-25.us-east-2.compute.amazonaws.com:8050/
Keep in mind this uses the free Twitter API and therefore doesn't have very large numbers of tweets for certain terms!







