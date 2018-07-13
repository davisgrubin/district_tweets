import os
import tweepy
import DistrictDict as dd
import sys
import boto3
from textblob import TextBlob
import json
import psycopg2
import numpy as np
import itertools
from time import sleep
from sentiment_timeseries import num_state_format




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
aws_key = os.environ['AWS_SECRET_ACCESS_KEY']
aws_key_id = os.environ['AWS_ACCESS_KEY']


conn = psycopg2.connect('dbname=davis user=davis host=/var/run/postgresql')
cur = conn.cursor()
# cur.execute('''CREATE TABLE tweetstest(
#     id SERIAL, content varchar, location varchar,
#     polarity real, subjectivity real, screen_name varchar,
#     district varchar,date_time timestamp);''')
# conn.commit()


class CustomStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.user.location != None:
            filt = [True if status.user.location in i[0] else False for i in dist_lookup]
            if any(filt):
                district = np.random.choice([i[1] for i in list(itertools.compress(dist_lookup,filt))])
                polarity = TextBlob(status.text).sentiment[0]
                subjectivity = TextBlob(status.text).sentiment[1]
                content = status.text
                location = status.user.location
                screen_name = status.user.screen_name
                date_time = status.created_at


                #For constantly updating to Kinesis Stream
                # data = {'text':str(status.text),'district':str(i[1]),
                # 'location':str(status.user.location),
                # 'polarity':TextBlob(status.text).sentiment[0],
                # 'subjectivity':TextBlob(status.text).sentiment[1],
                # 'time':str(status.created_at)}
                # client.put_record(DeliveryStreamName ='tweet_stream',
                # Record = {'Data':json.dumps(data)})
                cur.execute('''INSERT INTO tweetstest(content,location,
                polarity,subjectivity,screen_name,district,date_time) VALUES(%s,%s,%s,
                %s,%s,%s,%s)''',(content,location,polarity,subjectivity,screen_name,
                district,date_time))
                conn.commit()



    def on_error(self, status_code):
        print(sys.stderr, 'Encountered error with status code:', status_code)
        return True # Don't kill the stream

    def on_timeout(self):
        print(sys.stderr, 'Timeout...')
        return True # Don't kill the stream

    def on_exception(self, exception):
        print(exception)
        return True

if __name__ == '__main__':
    #Establishing Kinesis Stream
    # client = boto3.client('firehose',region_name ='us-east-2',aws_access_key_id=aws_key_id,
    # aws_secret_access_key=aws_key)
    backoff = 1
    while True:
        api = tweepy.API(auth)
        try:
            sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
            sapi.filter(locations=[-125,24,-66,50])
        except:
            e = sys.exc_info()[0]
            print('I just caught the exception: %s' % e)
            backoff += 1
            sleep(60 * backoff)
            continue
