from utils.common.ssh import SecureShell

from os.path import join

class JSAnalyzer:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #Obtain JavaScript files from multiple sources. Return the path of the scan result.
    def reun_get_javascript(self, url: str) -> str:
        path_out = join(self.results_path, 'getjs.txt')
        out = self.ssh.execute_wait_command(f'getJS --complete --url {url} | tee {path_out}')
        return path_out

    #TODO
    def analyze_javascript(self, path):
        pass