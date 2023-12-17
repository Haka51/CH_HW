use test;
drop table test.antonovao;

CREATE table test.antonovao(
a Decimal32(4), b String, c enum('a'=1,'b'=2,'c'=3, 'd'=4)
) Engine = Log()
as select
cast(randUniform(0,1000) as Decimal32(4)) as a,
randomPrintableASCII(randUniform(5,10)) as b,
[1,2,3,4][toInt64(randBinomial(3,0.5))+1] as c
from numbers(10000);
 

select *
from test.antonovao
where 1=1
and a > 10
and b ilike '%abs%'
limit 10;

INSERT into test.antonovao
select
cast(randUniform(0,1000) as Decimal32(4)) a,
randomPrintableASCII(randUniform(5,10)) b,
[1,2,3,4][toInt64(randBinomial(3,0.5))+1] c
from numbers(10000);

select *
from test.antonovao
where 1=1
and a > 10
and b ilike '%abs%'
limit 10;

INSERT into test.antonovao
select
14 a,
'sdanihuabssadi' b,
1 c;