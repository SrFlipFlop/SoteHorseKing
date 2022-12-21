from utils.common.ssh import SecureShell

from os.path import join

class Sslscan:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def sslscan_default(self, url):
        path_out = join(self.results_path, 'sslscan_default.txt')
        path_xml = join(self.results_path, 'sslscan_default.xml')
        stdin, stdout, stderr = self.ssh.execute_command(f'sslscan --xml={path_xml} {url} | tee {path_out}')