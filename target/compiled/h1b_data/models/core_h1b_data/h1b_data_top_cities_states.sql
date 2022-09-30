

WITH states AS(
  SELECT
     state_code
    ,state_text
  FROM `wise-logic-354820`.`dbt_h1b_data`.`states`
),

qol AS(
  SELECT
     overall_rank
    ,state_code
    ,total_score
    ,affordability
    ,economy
    ,education_health
    ,quality_of_life
    ,state_safety
  FROM `wise-logic-354820`.`dbt_h1b_data`.`wallet_hub_qol`
),

states_qol AS(
  SELECT
     overall_rank
    ,s.state_code
    ,state_text
    ,total_score
    ,affordability
    ,economy
    ,education_health
    ,quality_of_life
    ,state_safety
  FROM `wise-logic-354820`.`dbt_h1b_data`.`states` s JOIN `wise-logic-354820`.`dbt_h1b_data`.`wallet_hub_qol` wh_qol
  ON s.state_code = wh_qol.state_code
)


SELECT 
   DATE_TRUNC(DECISION_DATE, YEAR) AS rc_yr
  ,VISA_CLASS AS visa_class
  ,EMPLOYER_NAME AS employer_name
  ,EMPLOYER_CITY AS employer_city
  ,EMPLOYER_STATE AS employer_state
  ,overall_rank AS wh_state_overall_rank
  ,state_code AS wh_state_state_code
  ,state_text AS wh_state_state_text
  ,total_score AS wh_state_total_score
  ,affordability AS wh_state_affordability
  ,economy AS wh_state_economy
  ,education_health AS wh_state_education_health
  ,quality_of_life AS wh_state_quality_of_life
  ,state_safety AS wh_state_safety
  ,SOC_TITLE AS soc_title
  ,FULL_TIME_POSITION AS full_time_position
  ,CASE_STATUS AS case_status
  ,COUNT(DISTINCT CASE_NUMBER) AS total_cases
  ,ROUND(AVG(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)),0) AS avg_decision_days
  ,MIN(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)) AS min_decision_days
  ,MAX(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)) AS max_decision_days
  ,ROUND(AVG(WAGE_RATE_OF_PAY_FROM),0) AS wage_rate_of_pay_from
  ,ROUND(AVG(WAGE_RATE_OF_PAY_TO),0) AS wage_rate_of_pay_to
  ,ROUND(MIN(WAGE_RATE_OF_PAY_FROM),0) AS min_wage_rate_of_pay_from
  ,ROUND(MAX(WAGE_RATE_OF_PAY_TO),0) AS max_wage_rate_of_pay_from
  ,ROUND(AVG(PREVAILING_WAGE),0) AS prevailing_wage
  
FROM `wise-logic-354820`.`dbt_h1b_data`.`h1b_data` h LEFT JOIN states_qol sq
ON h.EMPLOYER_STATE = sq.state_text
WHERE VISA_CLASS = 'H-1B'
GROUP BY 1,2,3,4,5,6,7,8