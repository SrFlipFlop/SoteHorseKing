from utils.common.ssh import SecureShell

from os.path import join

class Wappalyzer:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #TODO
    def analyze_technology(self, url):
        path_out = join(self.results_path, 'technologies.wappy')
        out = self.ssh.execute_wait_command(f'wappy -o {path_out} -j {url}')

        json = ''.join(map(str, out['stdout'].readlines()))
        #Parse JSON and return only the technologies