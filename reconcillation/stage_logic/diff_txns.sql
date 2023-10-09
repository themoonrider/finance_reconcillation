select
    t.completed_at as Completed_At,
    t.id as Transaction_ID,
    round(t.amount, 2) as FFI_Amount,
    round(tp.amount, 2) as TP_Amount,
    u.id as User_ID,
    u.type as User_Type,
    t.status as `Status` 

from 
    {transactions_table_id} t
join 
    {source_table_id} tp 
on 
    t.id = tp.id
left join 
    {users_table_id} u
on 
    t.user_id = u.id
where 
   tp.`timestamp` between '{start_date}' and '{end_date}'
    and t.amount <> tp.amount
