// 3statystyki wojewodztw
match (t:Tweet)<-[tw:TWEETED]-(u:User)-[l:LIVES_IN]->(p:Province)
with count(t) as t_all, p.name as woj, count(t) as l_tweet
match (t1:Tweet)<-[tw:TWEETED]-(u:User)-[l:LIVES_IN]->(p:Province)
where t1.is_political = 'True' and p.name = woj
with t_all, woj,l_tweet, count(t1) as l_tweet_p, round(count(t1)*10000.0/l_tweet)/100 as `pol/all`
match (t2:Tweet)<-[tw:TWEETED]-(u:User)-[l:LIVES_IN]->(p:Province)
where t2.is_domestic = 'True' and p.name = woj
return woj, l_tweet, l_tweet_p, `pol/all`, count(t2) as l_tweet_k, round(count(t2)*10000.0/l_tweet)/100 as `kraj/all`
order by l_tweet desc