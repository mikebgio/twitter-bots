import tweepy
import time
import sqlite3

# login to twitter account api
auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
api = tweepy.API(auth)
print("Connected: {}".format(api))

# SQLITE
table = 'meganamram'

def grab_rows(conn):
    sql = '''
        SELECT *
        FROM {tn}
        WHERE is_trump=1
    '''.format(tn=table)
    curs = conn.cursor()
    return curs.execute(sql)

def update_rows(conn, tweetdata):
    sql = '''UPDATE {tn}
            SET retweet_count = ? ,
                favorite_count = ?
            WHERE id = ?'''.format(tn=table)
    curs = conn.cursor()
    curs.execute(sql, tweetdata)
    conn.commit()



def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def main():
    database = 'tweets.db'
    # create a database connection
    conn = create_connection(database)
    with conn:
        data = grab_rows(conn)
        rows = data.fetchall()
        for row in rows:
            try:
                tweet = api.get_status(row[0])
            except tweepy.RateLimitError:
                print(TweepError.message[0]['code'])
                time.sleep(60 * 15)
                continue
            old_rc_fc = (row[4],row[5])
            new_rc_fc = (tweet.retweet_count, tweet.favorite_count)
            tweetdata = new_rc_fc + (tweet.id,)
            if old_rc_fc == new_rc_fc:
                print("Tweet {} has not changed!".format(tweet.id))
            else:
                print("Updating tweet: {}\nRetweets: {}\nFavorites: {}\n".format(tweet.id, new_rc_fc[0], new_rc_fc[1]))
                update_rows(conn, tweetdata)

if __name__ == '__main__':
    main()

