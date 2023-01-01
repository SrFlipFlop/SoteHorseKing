from utils.common.ssh import SecureShell

from os.path import join

class Sslscan:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #Launch default sslscan. Return the results in XML format.
    def run_sslscan_default(self, url: str) -> str:
        path_out = join(self.results_path, 'sslscan_default.txt')
        path_xml = join(self.results_path, 'sslscan_default.xml')
        out = self.ssh.execute_wait_command(f'sslscan --xml={path_xml} {url} | tee {path_out}')
        return path_xml