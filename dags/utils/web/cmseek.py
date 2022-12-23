from utils.common.ssh import SecureShell

from os.path import join

class CMSeek:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def cmseek_default(self, url):
        path_out = join(self.results_path, 'cmseek-default.txt')
        stdin, stdout, stderr = self.ssh.execute_command(f'cmseek -u {url} --follow-redirect -r | tee {path_out}')