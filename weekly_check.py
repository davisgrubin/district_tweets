import psycopg2
import os
import preprocess_twitter as pre
import numpy

conn = psycopg2.connect('dbname=davis user=davis host=/var/run/postgresql')
cur = conn.cursor()




cur.execute('''UPDATE tweetstest SET party = (SELECT dist_parties.party
FROM dist_parties WHERE dist_parties.district = tweetstest.district)''')
conn.commit()

#Get Number of Democratic Tweets
cur.execute('''SELECT COUNT(*) FROM tweetstest WHERE party = True''')
num_dem_tweets = cur.fetchall()
num_dem_tweets = num_dem_tweets[0][0]
conn.commit()

#Get Number of Republican Tweets
cur.execute('''SELECT COUNT(*) FROM tweetstest WHERE party = False''')
num_rep_tweets = cur.fetchall()
num_rep_tweets = num_rep_tweets[0][0]
conn.commit()

if os.path.exists('num_of_tweets.txt'):
    with open("num_of_tweets.txt",'r') as f:
        old_num_dem_tweets = f.readline()
        old_num_rep_tweets = f.readline()
    with open("num_of_tweets.txt",'w') as f:
        f.write(str(num_dem_tweets))
        f.write('\n')
        f.write(str(num_rep_tweets))
        f.close()

else:
    with open("num_of_tweets.txt",'w') as f:
        f.write(str(num_dem_tweets))
        f.write('\n')
        f.write(str(num_rep_tweets))
        f.close()