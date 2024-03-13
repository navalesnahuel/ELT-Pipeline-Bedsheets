with product_details as (
	select 
		product_id,
		p.name as product_name,
		p.category_id,
		c.name as category_name,
		p.material_id,
		m.name as material_name,
		p.size_id,
		s.name as size_name,
		cost_price
	from {{ ref('stg_bedsheets__products') }} p
		left join {{ ref('stg_bedsheets__sizes') }} s 
		    on p.size_id  = s.size_id 
		left join {{ ref('stg_bedsheets__materials') }} m
		    on p.material_id  = m.material_id 
		left join {{ ref('stg_bedsheets__categories') }} c 
		    on p.category_id  = c.category_id 
),

final as (
	select 
		*
	from product_details
)

select * from final