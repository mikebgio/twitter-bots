
TRACK_TERMS = ["trump", "clinton", "sanders", "hillary clinton", "bernie", "donald trump"]
CONNECTION_STRING = "sqlite:///trump.db"
CSV_NAME = "tweets.csv"
TABLE_NAME = "tweets"

try:
    from private import *
except Exception:
	pass