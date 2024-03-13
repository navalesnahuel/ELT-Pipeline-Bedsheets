{{
  config(
    materialized = 'view',
    )
}}

WITH materials as (
    select 
        material_id,
        name
    from {{ source('bedsheets', 'raw_materials') }}
    order by material_id asc
    ),

final as (
    select 
        * 
    from materials
)

select * from final
