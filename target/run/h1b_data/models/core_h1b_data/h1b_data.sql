

  create or replace table `wise-logic-354820`.`dbt_h1b_data`.`h1b_data`
  
  
  OPTIONS()
  as (
    

SELECT *
FROM `wise-logic-354820`.`dbt_h1b_data`.`stg_h1b_data`
  );
  