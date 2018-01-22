# district_tweets
Collection and analysis of tweets by congressional district
#### What can tweets tell us about the partisan make-up congressional district where they come from? 
#### Could they potentially provide insight into future election outcomes that polls may be unable to?
  *Main challenges: 
*collecting tweets and filtering into congressional districts.
*Feature engineering to create preditive model.
*Creating visualizations to better understand and compare each district.

# Collecting Data
## Twitter Streaming API w/ Tweepy
The Twitter Streaming API allows for the collection of tweets by specifiying bounding boxes - in my case I enclosed the continental U.S. 
and then filtered on tweet metadata. While a very small amount of this data has exact geographic coordinates, many do have user specified locations. By creating a index of place names by congressional district using the [relationship](https://www.census.gov/geo/maps-data/data/relationship.html) and [name-lookup](https://www.census.gov/geo/maps-data/data/nlt.html) files made public by census.gov, I was able to create a pipeline that saved tweets originating from accounts with these locations as .txt files with the State FIPS code and distrcit number as a title. Currently I have around 9GB of tweets and corresponding metadata. Since I went down many rabbit-holes trying to find more sophisticated ways of filtering that used the Twitter Api itself instead 

# Methods
First I loaded the tweets into a dataframe and did some standard text pre-processing by removing links and english stopwords.
By treating each district's tweets as a document, I created a TF-IDF matrix and a bag-of-words and used a Multinomial Naive Bayes and SVM  classifier trained using Stochastic Gradient Descent on each for a baseline. The labels were whether that district was represented by a Democrat(0) or a Republican(1).

For the model evaluation I split the districts and their associated tweets into a training set of 307. Surprisingly the most simple approach, a bag of words with Naive Bayes had a 3 fold cross validated score of 70 % while the Tfidf with a SVM performed at 72% accuracy. I've also incorporated sentiment analysis using VADER analysis on tweets from each district containing the terms "Trump", "clinton", "republican" and "democrat", though these features do not appear to be making much of a difference as of right now. Performing latent semantic analysis to reduce the feature dimensions to 2000, 1000, 100, 50 did not improve accuracy rates either. 

# Goals
Changing my dependent variable to COOK PVI, a measure of congressional partisanship in each district that is calculated by comparing district-level presidential election results to those of the national presidential election. Also trying Latent Dirichlet Allocation instead of Latent Semantic Analysis. I've also been using a small amount of my total dataset to train (about 1/4) so I may be able to increase accuracy just by introducing more tweets.

I'd also like to use Bokeh or Folium to create an interactive visualization that allows users to look at topics, communities, sentiment analysis of topics, most shared links, similar/dissimilar districts (based on cosine similarities/Cook PVI), predicted vs real Cook PVI etc.. as what time I have limited. 





