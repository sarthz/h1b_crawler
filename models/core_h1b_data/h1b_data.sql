{{ config(materialized='table') }}

SELECT *
FROM {{ ref('stg_h1b_data') }}