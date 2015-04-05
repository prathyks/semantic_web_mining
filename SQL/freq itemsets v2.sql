use epinions_2;

select iduser, count(distinct idproduct) 
from review
group by iduser
having count(distinct idproduct) = 1
;--56646 users

select iduser, count(distinct idproduct) 
from review
group by iduser
having count(distinct idproduct) > 1
;--56983 users

--getting 2 combinations of userids reviewed to a product
select concat(concat(x.iduser,','),y.iduser) as ids, count(x.idproduct)
from review x
join review y
on x.idproduct = y.idproduct
where (x.iduser, y.iduser) in (
select a.iduser, b.iduser
from review a
join review b
on a.iduser > b.iduser and
a.idproduct = b.idproduct
where a.idproduct = 686)
group by ids
order by 1,2;

--getting 2 combinations of userids reviewed to a product
select concat(concat(x.iduser,','),y.iduser) as ids, count(x.idproduct)
from review x
join review y
on x.idproduct = y.idproduct
where (x.iduser, y.iduser) in (
select a.iduser, b.iduser
from review a
join review b
on a.iduser > b.iduser and
a.idproduct = b.idproduct)
group by ids
order by 1,2;

--getting 2 combinations of userids reviewed to a product
select concat(concat(concat(concat(x.iduser,','),y.iduser),','),z.iduser) as ids, count(x.idproduct)
from review x
join review y
on x.idproduct = y.idproduct
join review z
on x.idproduct = z.idproduct
where (x.iduser, y.iduser, z.iduser) in (
select a.iduser, b.iduser, c.iduser
from review a
join review b
on a.iduser > b.iduser and
a.idproduct = b.idproduct
join review c
on a.iduser > c.iduser and
a.idproduct = c.idproduct
)
group by ids
order by 1,2;