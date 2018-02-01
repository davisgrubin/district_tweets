import pandas as pd
from collections import defaultdict
import os
import json
import pickle

def tweets2df():
    tweets_data = dict()
    for i in os.listdir('stream_tweets'):
        with open('stream_tweets/{0}'.format(i),mode='r') as json_data:
            district = i.split(".")[0]
            tweets_data[district] = []
            for line in json_data:
                tweet = json.loads(line)
                tweets_data[district].append((tweet['user']['location'], tweet['text']))
    tweets_df = pd.DataFrame()
    text = []
    dists = []
    for k, v in tweets_data.items():
        text.append(list(map(lambda tweet: tweet[1], v)))
        dists.append(k)
    tweets_df['text'] = text
    tweets_df['district'] = dists
    tweets_df.to_pickle('tweets_df.pikl')
def get_parties():
    state_codes = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '2', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '8',
    'CA': '6', 'AL': '1', 'AR': '5', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '4', 'ID': '16', 'CT': '9',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
    }
    df = pd.read_csv('legislators-current.csv')
    df = df[df['type'] != 'sen']
    df = df[df['state'] != 'GU']
    df = df[df['state'] != 'MP']
    df = df[df['state'] != 'PR']
    df = df[df['state'] != 'AS']
    df = df[df['state'] != 'VI']
    df['state'] = [state_codes[i] for i in df['state']]
    party_dict = {"Democrat":0,"Republican":1}
    df['party'] = [party_dict[i] for i in df['party']]
    df['district'] = [str(int(i)) for i in df['district']]
    df['district'] = ['0'+i if len(i) < 2 else i for i in df['district']]
    df['state_dist'] = df['state'] + '-' + df['district']
    df = df[['state_dist','party']]
    return df

def get_tweets(no_districts=False):
    with open('tweets_df.pikl','rb') as pickle_file:
        tweets_df = pickle.load(pickle_file)
    by_party = get_parties()
    by_party = by_party.rename(columns={"state_dist":"district"})
    tweets_df = tweets_df.merge(by_party,how='left',on='district')
    if no_districts == True:
        tweets_df.drop('district',axis=1,inplace=True)
    return tweets_df


if __name__ == '__main__':
    tweets_df = get_tweets()
