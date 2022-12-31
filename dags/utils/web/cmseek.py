from utils.common.ssh import SecureShell

from os.path import join

class CMSeek:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #Execute cmseek to find CMS used by the web application. Return the path of the result.
    def run_cmseek_default(self, url: str) -> str:
        path_out = join(self.results_path, 'cmseek.txt')
        out = self.ssh.execute_wait_command(f'cmseek -u {url} --follow-redirect -r | tee {path_out}')
        return path_out