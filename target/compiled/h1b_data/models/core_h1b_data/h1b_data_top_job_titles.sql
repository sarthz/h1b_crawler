

SELECT
   DATE_TRUNC(DECISION_DATE, MONTH) AS rc_yr_mnth
  ,VISA_CLASS as visa_class
  ,EMPLOYER_NAME as employer_name
  -- ,JOB_TITLE as job_title --title can differ from company to company
  ,SOC_TITLE as soc_title
  ,FULL_TIME_POSITION as full_time_position
  ,CASE_STATUS as case_status
  ,COUNT(DISTINCT CASE_NUMBER) as total_cases
  ,ROUND(AVG(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)),0) as avg_decision_days
  ,MIN(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)) as min_decision_days
  ,MAX(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)) as max_decision_days
  ,ROUND(AVG(WAGE_RATE_OF_PAY_FROM),0) as wage_rate_of_pay_from
  ,ROUND(AVG(WAGE_RATE_OF_PAY_TO),0) as wage_rate_of_pay_to
  ,ROUND(MIN(WAGE_RATE_OF_PAY_FROM),0) as min_wage_rate_of_pay_from
  ,ROUND(MAX(WAGE_RATE_OF_PAY_TO),0) as max_wage_rate_of_pay_from
  ,ROUND(AVG(PREVAILING_WAGE),0) as prevailing_wage
  
-- FROM `h1b_data.h1b_data_at_sample`
FROM `wise-logic-354820`.`dbt_h1b_data`.`h1b_data`
WHERE VISA_CLASS = 'H-1B'
GROUP BY 1,2,3,4,5,6