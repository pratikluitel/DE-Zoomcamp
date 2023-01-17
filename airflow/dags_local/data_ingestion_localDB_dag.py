import os
from airflow import DAG

from datetime import datetime

#operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingestion_script import ingest_callable

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME','/opt/airflow')

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

local_workflow = DAG(
    dag_id = "LocalIngestionDAG",
    schedule_interval= "0 6 2 * *", # this takes a cron expression https://crontab.guru/#0_6_2_*_*
     start_date= datetime(2021, 1, 1)
)

URL_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
URL_TEMPLATE = URL_PREFIX + "/yellow_tripdata_{{execution_date.strftime('%Y-%m')}}.csv.gz" # jinja is supported. execution_date gives date of execution

FILE_TEMPLATE = AIRFLOW_HOME+"/output_{{execution_date.strftime('%Y-%m')}}.csv.gz"

TABLE_TEMPLATE = "yellow_taxi_{{execution_date.strftime('%Y_%m')}}"

with local_workflow:
    
    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'curl -sSL {URL_TEMPLATE} > {FILE_TEMPLATE}',
    )
    
    ingest_task = PythonOperator(
        task_id='ingest',
        python_callable=ingest_callable,
        op_kwargs= {
            'user': PG_USER,
            'password': PG_PASSWORD,
            'host': PG_HOST,
            'port': PG_PORT,
            'db': PG_DATABASE,
            'table_name': TABLE_TEMPLATE,
            'csv_file': FILE_TEMPLATE
        }
    )
    
    #workflow definition at the end
    wget_task >> ingest_task

