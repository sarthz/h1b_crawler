"""
CREATE OR REPLACE TABLE h1b_data.h1b_data_at_cities_states AS
SELECT
   DATE_TRUNC(DECISION_DATE, YEAR) AS rc_yr
  ,VISA_CLASS AS visa_class
  ,EMPLOYER_NAME AS employer_name
  ,EMPLOYER_CITY AS employer_city
  ,EMPLOYER_STATE AS employer_state
  -- ,JOB_TITLE AS job_title --title can differ from company to company
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
  
-- FROM `h1b_data.h1b_data_at_sample`
FROM `h1b_data.h1b_data_airflow_transformed`
WHERE VISA_CLASS = 'H-1B'
GROUP BY 1,2,3,4,5,6,7,8
-- ORDER BY 1,2,3,4
-- ORDER BY 13 DESC,7 DESC,3,2,1
"""