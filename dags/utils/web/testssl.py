from utils.common.ssh import SecureShell

from os.path import join

class Testssl:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #Launch default testssl scan. Return the results in JSON format.
    def run_testssl_default(self, url: str) -> str:
        path_out = join(self.results_path, 'testssl_default.txt')
        path_json = join(self.results_path, 'testssl_default.json')
        out = self.ssh.execute_wait_command(f'testssl -oL {path_out} -oJ {path_json} {url}')
        return path_json