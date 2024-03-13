with joined_table as (
	select
	    order_id, 
        customer_id, 
        o.product_id, 
        name as product_name, 
        quantity as units, 
        cost_price as cost_price, 
        unit_price as retail_price, 
        order_date
	from {{ ref('stg_bedsheets__orders') }} o
	    left join {{ ref('stg_bedsheets__products') }} p 
	        on o.product_id = p.product_id
),

orders_table as (
    select 
        order_id,
        product_name,
        product_id,
        name as customer_name,
        t.customer_id,
        units,
        cost_price,
        retail_price,
        order_date
    from joined_table t
        left join {{ ref('stg_bedsheets__customers') }} c
            on t.customer_id = c.customer_id 
        order by order_date asc 
),

final as (
	select 
		*
	from orders_table
)

select * from final