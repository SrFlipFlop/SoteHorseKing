from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

args = {
    'owner': 'SrFlipFlop',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='test',
    default_args=args,
    start_date=datetime(2022,1,1,0),
    schedule_interval='@daily'
) as dag:
    task = BashOperator(
        task_id='test_task',
        bash_command='ssh linuxserver.io@openssh-server -p 2222 "./test.sh"'
    )