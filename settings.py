
TRACK_TERMS = ["trump", "clinton", "sanders", "hillary clinton", "bernie", "donald trump"]
CONNECTION_STRING = "sqlite:///twitter.db"
CSV_NAME = "tweets.csv"
TRUMP_TABLE_NAME = "trumps"
TRUMP_ID = '25073877'
MEG_ID = '35206553'
MEG_TABLE_NAME = "megs"
TEST_CONNECTION_STRING = "sqlite:///testing.db"

try:
    from private import *
except Exception:
	pass