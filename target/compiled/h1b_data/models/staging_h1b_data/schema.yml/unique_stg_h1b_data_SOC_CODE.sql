
    
    

with dbt_test__target as (

  select SOC_CODE as unique_field
  from `wise-logic-354820`.`dbt_h1b_data`.`stg_h1b_data`
  where SOC_CODE is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


