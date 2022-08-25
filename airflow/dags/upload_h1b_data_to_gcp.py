import os
import logging

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

import pandas as pd

from datetime import datetime
from google.cloud import storage


PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = "h1b_lca_data"
AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

URL_PREFIX = 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY'
URL_TEMPLATE = URL_PREFIX + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q' + str('{{ execution_date.strftime(\'%-m\') }}') +'.xlsx'
# OUTPUT_FILE_TEMPLATE_FP = 'green_tripdata_'+str('{{ execution_date.strftime(\'%Y-%m\') }}')+'.parquet'


dataset_file = 'LCA_Disclosure_Data_FY' + str('{{ execution_date.strftime(\'%Y\') }}') + '_Q' + str('{{ execution_date.strftime(\'%-m\') }}') +'.xlsx'
OUTPUT_FILE = dataset_file.replace(".xlsx", ".parquet")
parquet_file = dataset_file.replace('.csv', '.parquet')
# OUTPUT_FILE = 'green_tripdata_'+str('{{ execution_date.strftime(\'%Y-%m\') }}')+'.parquet'
#OUTPUT_FILE = 'bar_crawl_data'

#URL format: https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2022_Q3.xlsx

def upload_to_gcs(bucket, object_name, local_file):

    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)

def format_xlsx_to_csv(src_file):
    import subprocess
    import sys
    import pip

    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    # pip.main(['install', "openpyxl"])
    print("Source file: ", src_file)
    if not src_file.endswith('.xlsx'):
        logging.error("Can only accept source files in XLSX format, for the moment")
        return
    csv_df = pd.read_excel(src_file)
    print('attempting to write dataframe to csv format')
    csv_df.to_csv(src_file.replace('.xlsx', '.csv'))
    print("Wrote to file: ", src_file.replace('.xlsx', '.csv'))
    
    # src_file=f'{src_file}.csv'

    # sheet = xlrd.open_workbook(src_file).sheet_by_index(0)
    
    # # writer object is created
    # col = csv.writer(open("T.csv", 'w', newline=""))
    
    # # writing the data into csv file
    # for row in range(sheet.nrows):
    #     # row by row write 
    #     # operation is perform
    #     col.writerow(sheet.row_values(row))
    

def format_csv_to_parquet(src_file):
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

# DAG START

h1b_lca_data_workflow = DAG(
    "h1b_lca_data",
    schedule_interval="0 6 10 */3 *",
    start_date=datetime(2021,1,1),
    end_date=datetime(2022,12,31)
)


with h1b_lca_data_workflow:

    entry_task = BashOperator(
        task_id="entry_task",
        # bash_command='echo entering the dag'
        # bash_command='echo "{{ execution_date.strftime(\'%-m\') }}"',
        bash_command=f'echo {path_to_local_home}/{dataset_file} '
        # bash_command= 'echo '+ str('{{ execution_date.strftime(\'%Y\') }}') + str('{{ execution_date.strftime(\'%-m\') }}')/3 + '.xlsx'
    )


    download_data_task = BashOperator(
        task_id='download_data_task',
        bash_command=f"curl -sSL {URL_TEMPLATE} > {path_to_local_home}/{dataset_file}"
    )

    format_xlsx_to_csv_task = PythonOperator(
        task_id="format_xlsx_to_csv_task",
        python_callable=format_xlsx_to_csv,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )

    format_csv_to_parquet_task = PythonOperator(
        task_id="format_csv_to_parquet_task",
        python_callable=format_csv_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        # bash_command='echo "{{ execution_date.strftime(\'%Y-%m\') }}"'
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"raw/{OUTPUT_FILE}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
    )

entry_task >> download_data_task >> format_xlsx_to_csv_task >> format_csv_to_parquet_task >> local_to_gcs_task

# DAG END