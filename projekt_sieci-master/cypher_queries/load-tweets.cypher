// load_tweets
:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///100k.csv" AS line
WITH line
MERGE (u:User{user_id:line.user_id})
ON CREATE SET u.location = line.location
MERGE (t:Tweet{tweet_id:line.tweet_id})
ON CREATE SET t.quoted = line.quoted,
			  t.ret = line.ret,
              t.retweet_id = line.retweet_id,
              t.text = line.text,
              t.is_domestic = line.is_domestic,
              t.is_polical = line.is_polical,
              t.time = line.time
MERGE (u)-[r_t:TWEETED]->(t)