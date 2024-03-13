with joined_table as (
	select 
        order_id, 
        o.product_id, 
        quantity, 
        unit_price, 
        order_date, 
        cost_price 
    from {{ ref('stg_bedsheets__orders') }} o
	    left join {{ ref('stg_bedsheets__products') }} p
	        on o.product_id = p.product_id
),

finances as (
	select 
      	FORMAT_DATE('%Y-%m', date(order_date)) AS year_month,
	    sum(unit_price * quantity) as revenue,
	    sum(cost_price * quantity) as cost
	from joined_table
        group by year_month
        order by year_month
),

profit as (
	select 
		year_month,
		(revenue - cost) as profit
	from finances
),

final as (
	select 
		* 
	from profit
)

select * from final
