use ciao;

select * from groups_sup3 limit 5;

create table groups_sup3_apriori(
group_id integer,
user_num integer,
user_id integer,
sup_count integer
);

drop table group_size;

create table group_size_sup3_apriori(
group_id integer,
group_size_val decimal(4,3)
);

select group_id,count(1)
from groups_sup3_apriori
group by group_id
order by 2 desc; # the first row has the max value 

# truncate table group_size_sup4

# select max(user_num) from groups_sup3_apriori;

# select max(group_size_val) from group_size_sup3

insert into group_size_sup3_apriori
select group_id, count(1)/5
from groups_sup3_apriori
group by group_id;