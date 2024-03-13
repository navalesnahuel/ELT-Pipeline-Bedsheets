with c_table as (
	select 
		c.customer_id,
		c.name as customer_name,
		c.email,
		c.address,
		c.phone
	from {{ ref('stg_bedsheets__customers') }} c 
),

customers_orders as (
	select 
		customer_id,
		sum(quantity * unit_price) as revenue
	from {{ ref('stg_bedsheets__orders') }} o 
		group by customer_id
),

customers_plus_orders as (
	select 
		c.customer_id,
		customer_name,
		c.email,
		c.address,
		c.phone,
		o.revenue
	from c_table c
		full join customers_orders o
			on c.customer_id = o.customer_id
),

final as (
	select 
		*
	from customers_plus_orders
)

select * from final