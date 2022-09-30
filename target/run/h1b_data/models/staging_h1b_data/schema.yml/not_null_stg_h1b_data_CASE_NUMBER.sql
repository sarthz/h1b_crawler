select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select CASE_NUMBER
from `wise-logic-354820`.`dbt_h1b_data`.`stg_h1b_data`
where CASE_NUMBER is null



      
    ) dbt_internal_test