// calc political/all ratio
match (t:Tweet)
with count(t) as all_t
match (t2:Tweet)
where t2.is_political = "True"
return count(t2)*100.0/all_t