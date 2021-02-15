// 4calc % pol kraj
match (t:Tweet)
with count(t) as all_t
match (t2:Tweet)
where t2.is_political = "True"
with all_t, count(t2)*100.0/all_t as `średni % politycznych tweetów`
match (t3:Tweet)
where t3.is_domestic = "True"
return `średni % politycznych tweetów`, count(t3)*100.0/all_t as `średni % krajowych tweetów`