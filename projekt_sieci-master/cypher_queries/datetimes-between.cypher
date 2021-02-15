// datetimes_between
match (t:Tweet)
where datetime({year: 2020, month: 4, day: 7}) > t.time >= datetime({year: 2020, month: 4, day: 6})
return t