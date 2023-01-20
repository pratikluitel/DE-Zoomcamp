import os

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from ingestion_script import ingest_taxi_lookup
from datetime import datetime

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME','/opt/airflow')

PG_HOST = os.getenv('PG_HOST')
PG_USER = os.getenv('PG_USER')
PG_PASSWORD = os.getenv('PG_PASSWORD')
PG_PORT = os.getenv('PG_PORT')
PG_DATABASE = os.getenv('PG_DATABASE')

local_workflow = DAG(
    dag_id = "LocalIngestionLookupDAG",
    schedule_interval= "@yearly", # this takes a cron expression https://crontab.guru/#0_6_*_1_*
    start_date= datetime(2019, 1, 1)
)

URL_TEMPLATE = "https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"
FILE_TEMPLATE = AIRFLOW_HOME +"/taxi_zone_lookup.csv"
TABLE_TEMPLATE = "taxi_zone_lookup"

with local_workflow:
    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'curl -sSL {URL_TEMPLATE} > {FILE_TEMPLATE}',
    )
    
    ingest_task = PythonOperator(
        task_id='ingest',
        python_callable=ingest_taxi_lookup,
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
    
    wget_task >> ingest_task