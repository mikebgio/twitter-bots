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

db = dataset.connect(settings.CONNECTION_STRING)
trump_table = db[settings.TRUMP_TABLE_NAME]
meg_table = db[settings.MEG_TABLE_NAME]
phrase = "today was the day donald trump finally became president"


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)
        if status.user.id == settings.TRUMP_ID:
            tweet_id = status.id
            date = status.created_at.date()
            time = status.created_at.time().isoformat('seconds')
            text = status.text
            retweets = status.retweet_count
            favorites = status.favorite_count
            reply_to = status.in_reply_to_status_id

            if hasattr(status, 'quoted_status_id'):
                quote_status = status.quoted_status_id
            else:
                quote_status = None

            try:
                trump_table.insert(dict(
                    tweet_id=tweet_id,
                    date=date,
                    time=time,
                    text=text,
                    retweets=retweets,
                    favorites=favorites,
                    reply_to=reply_to,
                    quote_status=quote_status
                ))
                db.commit()
            except ProgrammingError as err:
                print(err)
                db.rollback()
        elif status.user.id == settings.MEG_ID:
            if phrase == tweet.text.lower():
                try:
                    meg_table.insert_ignore(dict(
                        tweet_id=tweet.id,
                        date=tweet.created_at.date(),
                        time=tweet.created_at.time().isoformat('seconds'),
                        text=tweet.text,
                        retweets=tweet.retweet_count,
                        favorites=tweet.favorite_count
                    ), ['tweet_id'])
                    db.commit()
                except ProgrammingError as err:
                    print(err)
                    db.rollback()

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('oh shit')
            return False

db.begin()
trumpStreamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=trumpStreamListener)
print('Starting stream...')
stream.filter(follow=[settings.TRUMP_ID, settings.MEG_ID])
