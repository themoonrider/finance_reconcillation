with prodA_gtv as (
select
    date(`timestamp`) as `date`,
    round(sum(amount), 2) as Total_ProdA_Amount
from 
    {tpa_table_id}
where 
    date(`timestamp`) between '{start_date}' and '{end_date}'
group by 1
)
,prodB_gtv as (
select
    date(`timestamp`) as `date`,
    round(sum(amount), 2) as Total_ProdB_Amount
from 
    {tpb_table_id}
where 
    date(`timestamp`) between '{start_date}' and '{end_date}'
group by 1
)
,dates as 
    (select 
        date(`date`) as `date` 
    from 
        date_range
    where `date` between '{start_date}' and '{end_date}'
    )
select 
d.date,
coalesce(a.Total_ProdA_Amount, 0.00) as Total_ProdA_Amount,
coalesce(b.Total_ProdB_Amount, 0.00) as Total_ProdB_Amount,
coalesce(a.Total_ProdA_Amount, 0.00) + coalesce(b.Total_ProdB_Amount, 0.00) as Total_Amount

from dates d
left join prodA_gtv a 
on d.date = a.date
left join prodB_gtv b
on d.date = b.date
order by 1