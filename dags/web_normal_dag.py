from datetime import datetime
from airflow.decorators import dag, task

from utils.web.nmap import Nmap

@dag(
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['web', 'normal'],
)

def web_normal():
    @task()
    def find_servers():
        nmap = Nmap()
        nmap.find_web_servers('127.0.0.1', '22,80,443', '/root/results')

    @task()
    def dir_enum():
        pass

    @task()
    def dir_enum_extension():
        pass

    find_servers()
    dir_enum()
    dir_enum_extension()

web_normal()
