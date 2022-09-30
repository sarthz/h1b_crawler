select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select SOC_CODE
from `wise-logic-354820`.`dbt_h1b_data`.`stg_h1b_data`
where SOC_CODE is null



      
    ) dbt_internal_test