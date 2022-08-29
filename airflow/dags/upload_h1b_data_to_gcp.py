import os
import logging

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

from datetime import datetime


PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = "h1b_lca_data"
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'h1b_data')

execution_year = ''+str('{{logical_date.strftime(\'%Y\')}}')
execution_month = ''+str('{{logical_date.strftime(\'%-m\')}}')
quarter = 0

#URL format: https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2022_Q3.xlsx
URL_PREFIX = 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY'
# URL_TEMPLATE = URL_PREFIX + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q' + str('{{ execution_date.strftime(\'%-m\') }}') +'.xlsx'
# URL_TEMPLATE = URL_PREFIX + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q' + str(quarter) +'.xlsx'
URL_TEMPLATE = URL_PREFIX + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q'

# dataset_file = 'LCA_Disclosure_Data_FY' + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q' + str('{{ execution_date.strftime(\'%-m\') }}') +'.xlsx'
# dataset_file = 'LCA_Disclosure_Data_FY' + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q' + str(quarter) +'.xlsx'
dataset_file = 'LCA_Disclosure_Data_FY' + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q'
OUTPUT_FILE = dataset_file.replace(".xlsx", ".parquet")
parquet_file = dataset_file.replace('.csv', '.parquet')
# gcs_parquet_file = 'LCA_Disclosure_Data_FY' + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q' + str('{{ execution_date.strftime(\'%-m\') }}') +'.parquet'
gcs_parquet_file = 'LCA_Disclosure_Data_FY' + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q'

def format_xlsx_to_csv(src_file):
    import pandas as pd
    import subprocess
    import sys
    import pip

    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    print("Source file: ", src_file)
    if not src_file.endswith('.xlsx'):
        logging.error("Can only accept source files in XLSX format, for the moment")
        return
    csv_df = pd.read_excel(src_file)
    print('attempting to write dataframe to csv format')
    csv_df.to_csv(src_file.replace('.xlsx', '.csv'))
    print("Wrote to file: ", src_file.replace('.xlsx', '.csv'))
        
def format_csv_to_parquet(src_file):
    import pandas as pd
    import pyarrow as pv
    import pyarrow.parquet as pq

    src_file = src_file.replace('.xlsx', '.csv')

    print("Source file to be fetched for format_csv_to_parquet: ", src_file)
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    print("Source file:",src_file)
    df = pd.read_csv(src_file)
    table = pv.Table.from_pandas(df)
    print("read from csv to df successful")
    pq.write_table(table, src_file.replace('.csv', '.parquet'))

# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    print("Source file to be fetched to upload to GCS: ", local_file)
    from google.cloud import storage
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def test(ex_year, ex_month, **kwargs):
    quarter=(((ex_month-1)//3)+1)
    year=ex_year
    kwargs['ti'].xcom_push(key='ex_month', value=quarter)
    kwargs['ti'].xcom_push(key='ex_year', value=year)

# DAG START

h1b_lca_data_workflow = DAG(
    "h1b_lca_data_v4",
    schedule_interval="0 6 10 */3 *",
    start_date=datetime(2021,1,1),
    end_date=datetime(2022,9,30),
    render_template_as_native_obj=True
)

with h1b_lca_data_workflow:

    entry_task = PythonOperator(
        task_id="entry_task",
        provide_context=True,
        # bash_command='echo '+str("{{logical_date.strftime(\'%-m\')|int}}")
        python_callable=test,
        op_kwargs={
            "ex_month": f"{execution_month}",
            "ex_year": f"{execution_year}",
        },
        # bash_command='echo '+"{% set logical_date | int}" #.strftime(\'%-m\')
        # bash_command=f'echo '+str('{{ logical_date.strftime(\'%Y\') }}') + '_Q' + str('{{ logical_date.strftime(\'%-m\') }}') +'.xlsx'
        # bash_command=f'echo {path_to_local_home}/{dataset_file} '
        # bash_command=f'echo '+str('{{ logical_date.strftime(\'%Y\') }}') + '_Q' + str('{{ logical_date.strftime(\'%-m\') }}') +'.xlsx'
    )

    entry_task2 = BashOperator(
        task_id='entry_task2',
        bash_command='echo "{{ ti.xcom_pull(key="ex_month") }}"'
    )

    download_data_task = BashOperator(
        task_id='download_data_task',
        params = {'quarter' : '{{ ti.xcom_pull(key="ex_month") }}'},
        # bash_command=f'echo "{URL_TEMPLATE}" + "{{ ti.xcom_pull(key="ex_month") }}" + ".xlsx" > {path_to_local_home}/{dataset_file}" + "{{ ti.xcom_pull(key="ex_month") }}" + ".xlsx"'
        # bash_command=f"curl -sSL {URL_TEMPLATE} > {path_to_local_home}/{dataset_file}"
        # bash_command=f"curl -sSL {URL_TEMPLATE} > {path_to_local_home}/{dataset_file}"
        # bash_command="curl -sSL https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY"+ str('{{ execution_date.strftime(\'%Y\') }}')+'_Q'+'{{ ti.xcom_pull(key="ex_month") }}.xlsx' + '>' + '/opt/airflow/'+'LCA_Disclosure_Data_FY' + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q'+'{{ ti.xcom_pull(key="ex_month") }}.xlsx'
        bash_command=f"curl -sSL {URL_TEMPLATE}"+'{{ ti.xcom_pull(key="ex_month") }}.xlsx' + '>' + f"{path_to_local_home}/{dataset_file}" + '{{ ti.xcom_pull(key="ex_month") }}.xlsx'
       )

    format_xlsx_to_csv_task = PythonOperator(
        task_id="format_xlsx_to_csv_task",
        python_callable=format_xlsx_to_csv,
        op_kwargs={
    #         "src_file": f"{path_to_local_home}/{dataset_file}",
            "src_file": f"{path_to_local_home}/{dataset_file}"+ '{{ ti.xcom_pull(key="ex_month") }}.xlsx',

        },
    )

    format_csv_to_parquet_task = PythonOperator(
        task_id="format_csv_to_parquet_task",
        python_callable=format_csv_to_parquet,
        op_kwargs={
            # "src_file": f"{path_to_local_home}/{dataset_file}",
            "src_file": f"{path_to_local_home}/{dataset_file}"+ '{{ ti.xcom_pull(key="ex_month") }}.csv',
        },
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{OUTPUT_FILE}"+ '{{ ti.xcom_pull(key="ex_month") }}.parquet',
            "local_file": f"{path_to_local_home}/{dataset_file}"+ '{{ ti.xcom_pull(key="ex_month") }}.parquet',
        },
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                # "tableId": "external_table",
                "tableId": f"external_"+ '{{ ti.xcom_pull(key="ex_year") }}' + '_Q' + '{{ ti.xcom_pull(key="ex_month") }}'
            },
            "externalDataConfiguration": {
                "autodetect": True,
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET}/raw/{gcs_parquet_file}"+ '{{ ti.xcom_pull(key="ex_month") }}.parquet'],
            },
        },
    )

entry_task >> entry_task2 >> download_data_task >> format_xlsx_to_csv_task >> format_csv_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task

# DAG END