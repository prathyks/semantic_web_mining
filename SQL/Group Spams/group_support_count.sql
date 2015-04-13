create table group_sup_count_sup3(
group_id integer,
sup_count_val decimal(4,3)
);

select max(sup_count)
from groups_sup3;

select * from groups_sup3
where user_num > 2
order by 4 desc; # the first row contains the max sup_count

insert into group_sup_count_sup3
select distinct group_id, sup_count/21
from groups_sup3
where user_num > 2
group by group_id
order by 1;

# select * from group_sup_count_sup3

create table group_sup_count_sup4(
group_id integer,
sup_count_val decimal(4,3)
);

select * from groups_sup4
where user_num > 2
order by 4 desc;

insert into group_sup_count_sup4
select distinct group_id, sup_count/11
from groups_sup4
where user_num > 2
group by group_id
order by 1;

# select * from group_sup_count_sup4

# drop table group_sup_count_sup4_apriori

create table group_sup_count_sup3_apriori(
group_id integer,
sup_count_val decimal(4,3)
);

select * from groups_sup3_apriori
where user_num > 2
order by 4 desc;

insert into group_sup_count_sup3_apriori
select distinct group_id, sup_count/21
from groups_sup3_apriori
where user_num > 2
group by group_id
order by 1;

# select group_id, max(sup_count_val) from group_sup_count_sup3_apriori;