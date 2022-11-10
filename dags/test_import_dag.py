from datetime import datetime
from airflow.decorators import dag, task

from utils.web.test import Test

@dag(
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=['example'],
)

def test_import():

    @task()
    def transform():
        return Test().test()

    @task()
    def load1(total_order_value: str):
        print(f"Total order value is: {total_order_value}")

    @task()
    def load2(total_order_value: str):
        print(f"LOAD2: {total_order_value}")

    var = transform()
    load1(var)
    load2(var)

test_import()