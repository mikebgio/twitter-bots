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

            if status.is_quote_status:
                quote_status = status.quoted_status_id
            else:
                quote_status = None

            table = db[settings.TABLE_NAME]
            try:
                table.insert(dict(
                    tweet_id=tweet_id,
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

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_data disconnects the stream
            print('oh shit')
            return False


trumpStreamListener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=trumpStreamListener)
print('Starting stream...')
stream.filter(follow=[settings.TRUMP_ID])
