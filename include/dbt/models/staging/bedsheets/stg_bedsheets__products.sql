{{
  config(
    materialized = 'view',
    )
}}

WITH products as (
    select 
        product_id,
        name,
        cost_price,
        category_id,
        material_id,
        size_id
    from {{ source('bedsheets', 'raw_products') }}
    order by product_id asc
    ),

final as (
    select 
        * 
    from products
)

select * from final
