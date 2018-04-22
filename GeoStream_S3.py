import os
import tweepy
import DistrictDict as dd
import sys
import boto3
from textblob import TextBlob
import json


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
aws_key = os.environ['AWS_SECRET_ACCESS_KEY']
aws_key_id = os.environ['AWS_ACCESS_KEY']

class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.user.location != None:
            for i in dist_lookup:
                if status.user.location in i[0]:
                        data = {'text':str(status.text),'district':str(i[1]),
                        'location':str(status.user.location),
                        'polarity':TextBlob(status.text).sentiment[0],
                        'subjectivity':TextBlob(status.text).sentiment[1],
                        'time':str(status.created_at)}
                        client.put_record(DeliveryStreamName ='tweet_stream',
                        Record = {'Data':json.dumps(data)})



    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True # Don't kill the stream

if __name__ == '__main__':
    client = boto3.client('firehose',region_name ='us-east-2',aws_access_key_id=aws_key_id,
    aws_secret_access_key=aws_key)
    sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
    sapi.filter(locations=[-125,24,-66,50])
