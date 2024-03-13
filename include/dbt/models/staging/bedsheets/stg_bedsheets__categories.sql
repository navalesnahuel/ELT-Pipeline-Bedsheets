{{
  config(
    materialized = 'view',
    )
}}

WITH categories as (
    select 
        category_id,
        name,
        description
    from {{ source('bedsheets', 'raw_categories') }}
    order by category_id asc
    ),

final as (
    select 
        * 
    from categories
)

select * from final
