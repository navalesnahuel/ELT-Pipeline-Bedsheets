{{
  config(
    materialized = 'view',
    )
}}

WITH customers as (
    select 
        customer_id,
        name,
        phone,
        email,
        address
    from {{ source('bedsheets', 'raw_customers') }}
    order by customer_id asc
    ),

final as (
    select 
        * 
    from customers
)

select * from final

