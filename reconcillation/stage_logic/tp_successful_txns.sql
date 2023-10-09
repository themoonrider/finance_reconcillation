select
    date(`timestamp`) as `date`,
    round(sum(case when u.type = 0 then tp.amount end), 2) Total_Type0_Amount,
    round(sum(case when u.type = 1 then tp.amount end), 2) Total_Type1_Amount,
    round(sum(t.amount), 2) as Total_Amount,
    round(sum(tp.amount), 2) as Total_TP_Amount

from {source_table_id} tp 
join {transactions_table_id} t
    on tp.id = t.id
join {users_table_id} u
    on t.user_id = u.id
where 
    tp.timestamp between '{start_date}' and '{end_date}'

