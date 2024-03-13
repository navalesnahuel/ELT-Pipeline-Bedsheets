with products_revenue as (
	select 
        product_id,
		sum(quantity) as products_sold,
		sum(quantity * unit_price) as revenue
	from {{ ref('stg_bedsheets__orders') }} 
        group by product_id 
        order by revenue desc
),

products_revenue_cost as (
	select 
		r.product_id,
		r.products_sold,
		r.revenue,
		(p.cost_price * r.products_sold) as cost
	from products_revenue r
	    left join {{ ref('stg_bedsheets__products') }} p
	        on r.product_id = p.product_id
),

products_profit as (
	select 
		*,
		(revenue - cost) as profit
	from products_revenue_cost
	    order by profit desc
),

final as (
	select 
		* 
	from products_profit
)

select * from final