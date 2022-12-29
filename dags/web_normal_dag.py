from time import sleep
from datetime import datetime
from airflow.decorators import dag, task

from utils.web.nmap import Nmap

@dag(
    catchup=False,
    schedule=None,
    schedule_interval=None,
    render_template_as_native_obj=True,
    dag_id='Default_web_application_pentest',
    start_date=datetime(2023, 1, 1),
    tags=['web', 'normal'],
    params={
        'url': 'https://default.test',
        'name': f'{datetime.now().strftime("%d-%m-%Y")}_default',
    },
)
def pentest():
    @task()
    def find_servers():
        pass

    @task()
    def dir_enum():
        pass

    @task()
    def dir_enum_extension():
        pass

    find_servers()

pentest()
