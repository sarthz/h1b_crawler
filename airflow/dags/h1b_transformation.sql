"""
CREATE OR REPLACE TABLE h1b_data.h1b_data_airflow_transformed AS
                
    SELECT 
     CASE_NUMBER
    ,CASE_STATUS	
    ,CAST(RECEIVED_DATE AS DATE) AS RECEIVED_DATE	
    ,CAST(DECISION_DATE AS DATE) AS DECISION_DATE
    ,CAST(ORIGINAL_CERT_DATE AS DATE) AS ORIGINAL_CERT_DATE
    ,VISA_CLASS	
    ,JOB_TITLE
    ,SOC_CODE	
    ,SOC_TITLE	
    ,FULL_TIME_POSITION	
    ,CAST(BEGIN_DATE AS DATE) AS BEGIN_DATE	
    ,CAST(END_DATE AS DATE) AS END_DATE	
    ,TOTAL_WORKER_POSITIONS	
    ,CAST(NEW_EMPLOYMENT AS BOOL) AS NEW_EMPLOYMENT
    ,CAST(CONTINUED_EMPLOYMENT AS BOOL) AS CONTINUED_EMPLOYMENT	
    ,CAST(CHANGE_PREVIOUS_EMPLOYMENT AS BOOL) AS CHANGE_PREVIOUS_EMPLOYMENT	
    ,CAST(NEW_CONCURRENT_EMPLOYMENT AS BOOL) AS NEW_CONCURRENT_EMPLOYMENT	
    ,CAST(CHANGE_EMPLOYER AS BOOL) AS CHANGE_EMPLOYER	
    ,CAST(AMENDED_PETITION AS BOOL) AS AMENDED_PETITION
    ,EMPLOYER_NAME	
    ,TRADE_NAME_DBA	
    ,EMPLOYER_ADDRESS1	
    ,EMPLOYER_ADDRESS2	
    ,EMPLOYER_CITY	
    ,EMPLOYER_STATE	
    ,EMPLOYER_POSTAL_CODE	
    ,EMPLOYER_COUNTRY	
    ,EMPLOYER_PROVINCE
    ,CAST(EMPLOYER_PHONE AS STRING) AS EMPLOYER_PHONE	
    ,CAST(EMPLOYER_PHONE_EXT AS STRING) AS EMPLOYER_PHONE_EXT	
    ,CAST(NAICS_CODE AS STRING) AS NAICS_CODE	
    ,EMPLOYER_POC_LAST_NAME	
    ,EMPLOYER_POC_FIRST_NAME	
    ,EMPLOYER_POC_MIDDLE_NAME	
    ,EMPLOYER_POC_JOB_TITLE	
    ,EMPLOYER_POC_ADDRESS_1	
    ,EMPLOYER_POC_ADDRESS_2	
    ,EMPLOYER_POC_CITY	
    ,EMPLOYER_POC_STATE	
    ,EMPLOYER_POC_POSTAL_CODE	
    ,EMPLOYER_POC_COUNTRY	
    ,EMPLOYER_POC_PROVINCE	
    ,CAST(EMPLOYER_POC_PHONE AS STRING) AS EMPLOYER_POC_PHONE	
    ,CAST(EMPLOYER_POC_PHONE_EXT AS STRING) AS EMPLOYER_POC_PHONE_EXT	
    ,EMPLOYER_POC_EMAIL	
    ,AGENT_REPRESENTING_EMPLOYER
    ,AGENT_ATTORNEY_LAST_NAME	
    ,AGENT_ATTORNEY_FIRST_NAME	
    ,AGENT_ATTORNEY_MIDDLE_NAME	
    ,AGENT_ATTORNEY_ADDRESS1	
    ,AGENT_ATTORNEY_ADDRESS2	
    ,AGENT_ATTORNEY_CITY	
    ,AGENT_ATTORNEY_STATE	
    ,AGENT_ATTORNEY_POSTAL_CODE	
    ,AGENT_ATTORNEY_COUNTRY	
    ,AGENT_ATTORNEY_PROVINCE	
    ,CAST(AGENT_ATTORNEY_PHONE AS STRING) AS AGENT_ATTORNEY_PHONE	
    ,CAST(AGENT_ATTORNEY_PHONE_EXT AS STRING) AS AGENT_ATTORNEY_PHONE_EXT	
    ,AGENT_ATTORNEY_EMAIL_ADDRESS	
    ,LAWFIRM_NAME_BUSINESS_NAME	
    ,STATE_OF_HIGHEST_COURT	
    ,NAME_OF_HIGHEST_STATE_COURT	
    -- ,WORKSITE_WORKERS	
    ,SECONDARY_ENTITY
    ,SECONDARY_ENTITY_BUSINESS_NAME	
    ,WORKSITE_ADDRESS1	
    ,WORKSITE_ADDRESS2	
    ,WORKSITE_CITY	
    ,WORKSITE_COUNTY	
    ,WORKSITE_STATE	
    ,WORKSITE_POSTAL_CODE	
    ,WAGE_RATE_OF_PAY_FROM	
    ,WAGE_RATE_OF_PAY_TO	
    ,WAGE_UNIT_OF_PAY	
    ,PREVAILING_WAGE	
    ,PW_UNIT_OF_PAY	
    ,PW_TRACKING_NUMBER	
    ,PW_WAGE_LEVEL	
    ,PW_OES_YEAR	
    ,PW_OTHER_SOURCE	
    ,CAST(PW_OTHER_YEAR AS INT) AS PW_OTHER_YEAR	
    ,PW_SURVEY_PUBLISHER	
    ,PW_SURVEY_NAME	
    ,TOTAL_WORKSITE_LOCATIONS	
    ,AGREE_TO_LC_STATEMENT
    ,H1B_DEPENDENT
    ,WILLFUL_VIOLATOR
    ,SUPPORT_H1B
    ,STATUTORY_BASIS	
    ,APPENDIX_A_ATTACHED
    ,PUBLIC_DISCLOSURE	
    ,PREPARER_LAST_NAME	
    ,PREPARER_FIRST_NAME	
    ,PREPARER_MIDDLE_INITIAL	
    ,PREPARER_BUSINESS_NAME	
    ,PREPARER_EMAIL

    FROM `h1b_data.external_h1b_data`
    """