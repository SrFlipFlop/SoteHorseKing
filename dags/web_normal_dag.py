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
    dag_id='Default_web_application_pentest',
    start_date=datetime(2022, 1, 1),
    tags=['web', 'normal'],
    params={
        'url': 'https://default.test',
        'name': f'{datetime.now().strftime("%d-%m-%Y")}_default',
    },
)
def pentest():
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
        nmap.run_web_fast(url, ports=[80,3000,8080])

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def enum_vhosts(url: str, path: str, *args: list, **kwargs: dict) -> None:
        gobuster = Gobuster(path)
        gobuster.run_vhost_enum(url=url)

        sieve = VhostSieve(path)
        sieve.run_vhost_enum(url)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def check_web_technology(url: str, path: str, *args: list, **kwargs: dict) -> None:
        wappy = Wappalyzer(path)
        wappy.run_find_technologies(url)

        whatweb = WhatWeb(path)
        whatweb.run_find_technologies(url)
        whatweb.run_find_technologies_aggressive(url)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def check_cms(url: str, path: str, *args: list, **kwargs: dict) -> None:
        seek = CMSeek(path)
        seek.run_cmseek_default(url)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def crawler(url: str, path: str, *args: list, **kwargs: dict) -> None:
        katana = Katana(path)
        katana.run_crawl_full(url)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def javascript(url: str, path: str, *args: list, **kwargs: dict) -> None:
        js = JSAnalyzer(path)
        js.reun_get_javascript(url)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def dir_enum_normal(url: str, path: str, *args: list, **kwargs: dict) -> None:
        gobuster = Gobuster(path)
        gobuster.run_dir_enum(url=url)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def dir_enum_extensions(url: str, path: str, *args: list, **kwargs: dict) -> None:
        dirb = Dirb(path)
        dirb.run_dir_enum_extension(url=url, extensions=['js', 'txt'])

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def vulnerability_scanner(url: str, path: str, *args: list, **kwargs: dict) -> None:
        nuclei = Nuclei(path)
        nuclei.run_nuclei_default(url)

        nikto = Nikto(path)
        nikto.run_nikto_default(url)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def vulnerability_cms_scanner(url: str, path: str, *args: list, **kwargs: dict) -> None:
        wpscan = WPScan(path)
        wpscan.wpscan_default(url)

    @task(trigger_rule='all_done', execution_timeout=timedelta(minutes=120))
    def server_tls(url: str, path: str, *args: list, **kwargs: dict) -> None:
        testssl = Testssl(path)
        testssl.run_testssl_default(url)

        sslscan = Sslscan(path)
        sslscan.run_sslscan_default(url)

    URL = '{{params.url}}'
    PROJECT_PATH = join('/opt/pentest/results', '{{params.name}}')
    
    step1 = create_results_dir(PROJECT_PATH)
    wait1 = wait(5, step1)
    
    step2 = find_servers(URL, PROJECT_PATH, wait1)
    step3 = enum_vhosts(URL, PROJECT_PATH, wait1)
    step4 = check_web_technology(URL, PROJECT_PATH, wait1)
    step5 = check_cms(URL, PROJECT_PATH, wait1)
    wait2 = wait(5, [step2, step3, step4, step5])
    
    step6 = crawler(URL, PROJECT_PATH, wait2)
    step7 = javascript(URL, PROJECT_PATH, wait2)
    wait3 = wait(5, [step6, step7])

    step8 = dir_enum_normal(URL, PROJECT_PATH, wait3)
    step9 = dir_enum_extensions(URL, PROJECT_PATH, wait3)
    wait4 = wait(5, [step8, step9])

    step10 = vulnerability_scanner(URL, PROJECT_PATH, wait4)
    wait5 = wait(5, step10)

    step11 = vulnerability_cms_scanner(URL, PROJECT_PATH, wait5)
    step12 = server_tls(URL, PROJECT_PATH, wait5)

pentest()