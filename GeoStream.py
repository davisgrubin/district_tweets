import os
import tweepy
import DistrictDict as dd
import sys
import jsonpickle


dist_dict = dd.get_files()
dist_lookup = []
for k, v in dist_dict.items():
    dist_lookup.append((v,k))
    
TWITTER_APP_KEY = os.environ['TW_CONSUMER_KEY']
TWITTER_APP_SECRET = os.environ['TW_CONSUMER_SECRET']
TWITTER_KEY= os.environ['TW_ACCESS_TOKEN']
TWITTER_SECRET = os.environ['TW_ACCESS_SECRET']
auth = tweepy.OAuthHandler(TWITTER_APP_KEY, TWITTER_APP_SECRET)
auth.set_access_token(TWITTER_KEY, TWITTER_SECRET)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        tweetCount=0
        if status.user.location != None:
            for i in dist_lookup:
                if status.user.location in i[0]:
                    with open('stream_tweets/{0}.txt'.format(i[1]),'a') as f:
                        f.write(jsonpickle.encode(status._json, unpicklable=False) + '\n')
                        tweetCount += 1
                        if tweetCount%1000 == 0: print('Tweets Downloaded:{0}'.format(tweetCount))


    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True # Don't kill the stream

if __name__ == '__main__':
    tweetCount = 0
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
    sapi.filter(locations=[-125,24,-66,50])
