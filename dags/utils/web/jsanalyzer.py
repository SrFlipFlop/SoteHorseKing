from utils.common.ssh import SecureShell

from os.path import join

class JSAnalyzer:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def get_javascript(self, url):
        path_out = join(self.results_path, 'getjs.txt')
        stdin, stdout, stderr = self.ssh.execute_command(f'getJS --complete --url {url} | tee {path_out}')

    #TODO
    def analyze_javascript(self, path):
        pass