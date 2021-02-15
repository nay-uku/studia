// load_user,woj_with_prov
:auto USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///100k.csv" AS line
WITH line
WHERE NOT line.woj IS NULL
MERGE (u:User{user_id:line.user_id})
ON CREATE SET u.location = line.location
MERGE (p:Province{name:line.woj})
MERGE (u)-[r_liv:LIVES_IN]->(p)