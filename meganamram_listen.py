import tweepy
import time
import sqlite3

# login to twitter account api
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
api = tweepy.API(auth)
print(api)
trump = "today was the day donald trump finally became president"
tweet_count = 0
my_id = '30074932'
meganamram = '35206553'

# SQLITE
conn = sqlite3.connect('tweets.db')
curs = conn.cursor()
table = 'trumped'
#table = 'meganamram'

def add_row(tweet):
    if tweet.text.lower() == trump:
        is_trump = 1
    else:
        is_trump = 0
    curs.execute("INSERT OR IGNORE INTO {tn} values((?),(?),(?),(?),(?),(?),(?))".format(tn=table), (tweet.id, str(tweet.created_at.date(
    )), str(tweet.created_at.time()), tweet.text, tweet.retweet_count, tweet.favorite_count, is_trump))
    conn.commit()


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        add_row(status)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('oh shit')
            return False




print('create object')
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
print('streaming')

myStream.filter(follow=[my_id])



conn.close()
