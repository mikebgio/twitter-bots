import settings
import tweepy
import time
import dataset
from sqlalchemy.exc import ProgrammingError


# login to twitter account api
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
api = tweepy.API(auth)

print("Connected: {}".format(api))

db = dataset.connect(settings.CONNECTION_STRING)
table = db[settings.TRUMP_TABLE_NAME]


def get_last_id():
    result = table.find_one(order_by='tweet_id')
    return result['tweet_id']

def add_row(tweet):
    if hasattr(tweet, 'quoted_status_id'):
        quote_status = tweet.quoted_status_id
    else:
        quote_status = None

    try:
        table.insert_ignore(dict(
            tweet_id=tweet.id,
            date=tweet.created_at.date(),
            time=tweet.created_at.time().isoformat('seconds'),
            text=tweet.text,
            retweets=tweet.retweet_count,
            favorites=tweet.favorite_count,
            reply_to=tweet.in_reply_to_status_id,
            quote_status=quote_status
        ), ['tweet_id'])
        db.commit()
    except ProgrammingError as err:
        print(err)
        db.rollback()


c = tweepy.Cursor(api.user_timeline, id=settings.TRUMP_ID, max_id=get_last_id()).items()


def main():
    db.begin()
    while True:
        try:
            tweet = c.next()
            print("TweetID: {}\n{}".format(tweet.id, tweet.text))
            add_row(tweet)
            print("REMAINING: {}".format(api.rate_limit_status()[
                'resources']['statuses']['/statuses/user_timeline']['remaining']))
        except tweepy.RateLimitError:
            # print(tweepy.TweepError.message[0]['code'])
            print('RATE LIMITING, PLEASE WAIT 15 Minutes...')
            time.sleep(60 * 15)
            continue
        except StopIteration:
            print(api.rate_limit_status()['resources']
                  ['statuses']['/statuses/user_timeline'])
            print("StopIteration")
            break
    db.commit()

if __name__ == '__main__':
    main()
