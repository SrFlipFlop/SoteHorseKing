from utils.common.ssh import SecureShell

from os.path import join

class Nikto:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def nikto_default(self, url):
        path_out = join(self.results_path, 'default.nikto')
        stdin, stdout, stderr = self.ssh.execute_command(f'nikto -nointeractive -o {path_out} -h {url}')