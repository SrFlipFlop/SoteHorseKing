from os import mkdir
from time import sleep
from os.path import join, exists
from datetime import datetime, timedelta
from airflow.decorators import dag, task

from utils.web.nmap import Nmap
from utils.web.dirb import Dirb
from utils.web.nikto import Nikto
from utils.web.wpscan import WPScan
from utils.web.cmseek import CMSeek
from utils.web.nuclei import Nuclei
from utils.web.katana import Katana
from utils.web.testssl import Testssl
from utils.web.sslscan import Sslscan
from utils.web.whatweb import WhatWeb
from utils.web.gobuster import Gobuster
from utils.common.ssh import SecureShell
from utils.web.jsanalyzer import JSAnalyzer
from utils.web.wappalyzer import Wappalyzer
from utils.web.vhostssieve import VhostSieve

@dag(
    catchup=False,
    schedule=None,
    render_template_as_native_obj=True,
    dag_id='Web_application_analyze',
    start_date=datetime(2022, 1, 1),
    tags=['web', 'analyze'],
    params={
        'url': 'https://default.test',
        'name': f'{datetime.now().strftime("%d-%m-%Y")}_default',
    },
)
def analyze():
    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def create_results_dir(path):
        if not exists(path):
            mkdir(path)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def wait(delay=0, *args: list, **kwargs: dict):
        if delay:
            sleep(delay)
    
    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def find_servers(url: str, path: str, *args: list, **kwargs: dict) -> None:
        nmap = Nmap(path)
        nmap.analyze_webservers(join(path, 'nmap_web_fast.gnmap'))

    URL = '{{params.url}}'
    PROJECT_PATH = join('/opt/pentest/results', '{{params.name}}')    

    step1 = create_results_dir(PROJECT_PATH)
    wait1 = wait(5, step1)

    step2 = find_servers(URL, PROJECT_PATH, wait1)

analyze()