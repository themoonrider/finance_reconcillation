select
tp.timestamp as `Timestamp`,
tp.id as Transaction_ID,
tp.amount as Amount

from {source_table_id} tp
where 
    tp.timestamp between '{start_date}' and '{end_date}'
    and tp.id not in (
        select
            distinct id
        from {transactions_table_id}
                    )