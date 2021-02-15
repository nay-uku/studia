docker exec -it mongodb mongo
show dbs
use time_processing
db.createCollection('twitter_stream')
db.createCollection('discord_stream')
db.createCollection('cassandra_statistics')
db.createCollection('neo4j_msg_analysis')
db.createCollection('faust_filter')
db.createCollection('neo4j_markov_bot')
db.createCollection('mongo_sentiment_analysis')
show tables
db.twitter_stream.find({}).pretty().limit(1)