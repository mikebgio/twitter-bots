import settings
import tweepy
import time
# import sqlite3
import dataset
from sqlalchemy.exc import ProgrammingError

# login to twitter account api
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
api = tweepy.API(auth)
print(api)
TRUMP_ID = '25073877'

db = dataset.connect(settings.CONNECTION_STRING)

# SQLITE
# TABLE = 'trumps'  # TABLE IN tweets.db
# DB = 'tweets.db' # HAS table trumps

### TESTING STUFF ###
# TABLE = 'tweets'. #TEST
# DB = 'trump.db' #TEST

# conn = sqlite3.connect(DB)
# curs = conn.cursor()



# def add_row(tweet):
#     if tweet.is_quote_status:
#         quote_status = tweet.quoted_status_id
#     else:
#         quote_status = None
#     curs.execute("INSERT OR IGNORE INTO {tn} values((?),(?),(?),(?),(?),(?),(?),(?))".format(tn=TABLE), (tweet.id,
#         str(tweet.created_at.date()), str(tweet.created_at.time()), tweet.text, tweet.retweet_count, tweet.favorite_count,
#         tweet.in_reply_to_status_id, quote_status))
#     conn.commit()


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        tweet_id = status.id
        date = status.created_at.date()
        time = status.created_at.time()
        text = status.text
        retweets = status.retweet_count
        favorites = status.favorite_count
        reply_to = status.in_reply_to_status_id

        if status.is_quote_status:
            quote_status = status.quoted_status_id
        else:
            quote_status = None

        table = db[settings.TABLE_NAME]
        try:
            table.insert_ignore(dict(
                    id=tweet_id,
                    date=date,
                    time=time,
                    text=text,
                    retweets=retweets,
                    favorites=favorites,
                    reply_to=reply_to,
                    quote_status=quote_status
                ))
        except ProgrammingError as err:
            print(err)

        # add_row(status)

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('oh shit')
            return False


trumpStreamListener = StreamListener()
stream = tweepy.Stream(auth = api.auth, listener=trumpStreamListener)
#stream.filter(follow=[TRUMP_ID])
stream.filter(track=settings.TRACK_TERMS)