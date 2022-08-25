import pandas as pd

df = pd.read_excel("/Users/sthakur/Documents/GitHub/personal/h1b_crawler/airflow/dags/LCA_Disclosure_Data_FY2021_Q1.xlsx")
print(len(df))