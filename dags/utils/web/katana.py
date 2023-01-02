from utils.common.ssh import SecureShell

from os.path import join

class Katana:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def run_crawl_full(self, url: str) -> str:
        path_out = join(self.results_path, 'katana-crawler-depth5.txt')
        out = self.ssh.execute_wait_command(f'katana -d 5 -jc -kf all -o {path_out} -u {url}')
        return path_out

    #TODO
    def analyze_lfi(self, data):
        pass

    #TODO
    def analyze_redirects(self, data):
        pass

    #TODO
    def analyze_idor(self, data):
        pass