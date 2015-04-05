use epinions_2;

select * from review;

select reviewcount, count(idproduct) 
from reviewcount
group by reviewcount;

create table reviewCount_3
(
idproduct integer,
iduser3 varchar(20)
);

insert into reviewCount_3
select idproduct, group_concat(iduser) 
from review
where idproduct in (select idproduct 
					from reviewcount
                    where reviewCount = 3)
group by idproduct;

select iduser3, count(idproduct)
from reviewCount_3
group by iduser3
having count(idproduct) > 1
order by 2 desc;

select *
from review 
where iduser = 4

select iduser3, count(idproduct) 
from reviewCount_3
group by iduser3
having count(idproduct) > 1
order by 2 desc;