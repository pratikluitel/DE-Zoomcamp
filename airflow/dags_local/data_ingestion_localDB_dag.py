import os
from airflow import DAG

from datetime import datetime

#operators
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

local_workflow = DAG(
    dag_id = "LocalIngestionDAG",
    schedule_interval= "0 6 2 * *", # this takes a cron expression https://crontab.guru/#0_6_2_*_*
     start_date= datetime(2021,1,1)
)

AIRFLOW_HOME = os.environ.get('AIRFLOW_HOME','/opt/airflow')

URL_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow"
URL_TEMPLATE = URL_PREFIX + "/yellow_tripdata_{{execution_date.strftime('%Y-%m')}}.csv.gz" # jinja is supported. execution_date gives date of execution

FILE_TEMPLATE = AIRFLOW_HOME+"/output_{{execution_date.strftime('%Y-%m')}}.csv.gz"

with local_workflow:
    
    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'curl -sS {URL_TEMPLATE} > {FILE_TEMPLATE}',
    )
    
    ingest_task = BashOperator(
        task_id='ingest',
        bash_command=f'ls {AIRFLOW_HOME}'
    )
    
    #workflow definition at the end
    wget_task >> ingest_task

