{{
  config(
    materialized = 'view',
    )
}}

WITH sizes as (
    select 
        size_id,
        name
    from {{ source('bedsheets', 'raw_sizes') }}
    order by size_id asc
    ),

final as (
    select 
        * 
    from sizes
)

select * from final
