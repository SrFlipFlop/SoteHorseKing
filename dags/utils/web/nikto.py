from utils.common.ssh import SecureShell

from os.path import join

class Nikto:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #Launch nikto scan to enumerate vulnerabilities. Return the output path.
    def run_nikto_default(self, url: str) -> str:
        path_out = join(self.results_path, 'nikto_default.txt')
        out = self.ssh.execute_wait_command(f'nikto -nointeractive -o {path_out} -h {url}')
        return path_out