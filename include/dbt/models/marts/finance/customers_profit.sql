with joined_table as (
	select 
		o.customer_id, 
		c.name as customer_name, 
		order_id, 
		o.product_id, 
		quantity, 
		unit_price, 
		order_date,
		cost_price
	from {{ ref('stg_bedsheets__orders') }} o
		left join {{ ref('stg_bedsheets__customers') }} c  
			on o.customer_id = c.customer_id
		left join {{ ref('stg_bedsheets__products') }} p 
			on o.product_id = p.product_id
),

customers_revenue as (
	select 
		customer_name,
        customer_id,
		sum(quantity * unit_price) as revenue,
		sum(quantity * cost_price) as cost
	from joined_table
		group by customer_name, customer_id
),

c_profit as (
	select 
		*,
		(revenue - cost) as profit
	from customers_revenue
	    order by profit desc
),

final as (
	select 
        * 
    from c_profit
)

select * from final