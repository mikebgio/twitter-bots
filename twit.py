import tweepy
import time
import sqlite3


# login to twitter account api
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
api = tweepy.API(auth)

print(api)
table = 'tweets'
my_db = 'trump.db'
trump_id = 25073877

tweet_count = 0

# SQLITE
conn = sqlite3.connect(my_db)
curs = conn.cursor()

def get_last_id():
    curs.execute(
        'SELECT * FROM {tn} ORDER BY id DESC LIMIT 1'.format(tn=table))
    row = curs.fetchall()
    return(row[0][0])


def add_row(tweet):
    try:
        quote_status = tweet.quoted_status_id
    except AttributeError:
        quote_status = None
        pass
    curs.execute("INSERT OR IGNORE INTO {tn} values((?),(?),(?),(?),(?),(?),(?),(?))".format(tn=table), (tweet.id, 
        str(tweet.created_at.date()), str(tweet.created_at.time()), tweet.text, tweet.retweet_count, tweet.favorite_count, 
        tweet.in_reply_to_status_id, quote_status))
    conn.commit()

last_id = get_last_id()
c = tweepy.Cursor(api.user_timeline, id=trump_id, since_id=last_id).items()


while True:
    try:
        tweet = c.next()
        tweet_count += 1
        print("TweetID: {}\nTweetsProcessed: {}".format(tweet.id, tweet_count))
        # print("REMAINING: {}".format(api.rate_limit_status()[
              # 'resources']['statuses']['/statuses/user_timeline']['remaining']))
        add_row(tweet)
    except tweepy.RateLimitError:
        # print("You've hit your limit of {}".format(api.rate_limit_status()['resources']['statuses']['/statuses/user_timeline']['limit']))
        # print("REMAINING: {}".format(api.rate_limit_status()[
              # 'resources']['statuses']['/statuses/user_timeline']['remaining']))
        print(TweepError.message[0]['code'])
        time.sleep(60 * 15)
        continue
    except StopIteration:
        print(api.rate_limit_status()['resources']
              ['statuses']['/statuses/user_timeline'])
        print("StopIteration")
        break


conn.close()
