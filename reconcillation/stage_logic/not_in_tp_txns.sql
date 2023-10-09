select
    completed_at as Completed_At,
    t.id as Transaction_ID,
    t.amount as Amount, 
    u.id as User_ID,
    u.type as User_Type,
    t.status as `Status`

from 
    {transactions_table_id} t 
left join
    {users_table_id} u
on t.user_id = u.id

where 
    t.completed_at between '{start_date}' and '{end_date}'
    and {filter} --keep only transactions in ffi of the relevant product
    and t.id not in (select 
                        distinct id 
                    from 
                        {source_table_id} 
                    )
