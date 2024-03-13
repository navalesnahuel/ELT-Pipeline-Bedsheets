{{
  config(
    materialized = 'view',
    )
}}

WITH orders as (
    select 
        order_id,
        customer_id,
        product_id,
        quantity,
        unit_price,
        order_date
    from {{ source('bedsheets', 'raw_orders') }}
    order by order_id asc
    ),

final as (
    select 
        * 
    from orders
)

select * from final
