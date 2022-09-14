"""
CREATE OR REPLACE TABLE h1b_data.h1b_data_at_top_companies AS
SELECT
   DATE_TRUNC(DECISION_DATE, MONTH) AS rc_yr_mnth
  ,VISA_CLASS as visa_class
  ,EMPLOYER_NAME as employer_name
  ,CASE_STATUS as case_status
  ,COUNT(DISTINCT CASE_NUMBER) as total_cases
  ,ROUND(AVG(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)),0) as avg_decision_days
  ,MIN(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)) as min_decision_days
  ,MAX(DATE_DIFF(DECISION_DATE, RECEIVED_DATE, DAY)) as max_decision_days
  ,ROUND(AVG(WAGE_RATE_OF_PAY_FROM),0) as wage_rate_of_pay_from
  ,ROUND(AVG(WAGE_RATE_OF_PAY_TO),0) as wage_rate_of_pay_to
  ,ROUND(MIN(WAGE_RATE_OF_PAY_FROM),0) as MIN_wage_rate_of_pay_from
  ,ROUND(MAX(WAGE_RATE_OF_PAY_TO),0) as MAX_wage_rate_of_pay_to
  ,ROUND(AVG(PREVAILING_WAGE),0) as prevailing_wage
  
-- FROM `h1b_data.h1b_data_at_sample`
FROM `h1b_data.h1b_data_airflow_transformed`
WHERE VISA_CLASS = 'H-1B'
GROUP BY 1,2,3,4
-- ORDER BY 1,2,3,4
-- ORDER BY 5 DESC,3,2,1
"""