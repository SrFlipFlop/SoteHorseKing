from utils.common.ssh import SecureShell

from os.path import join

class Testssl:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def testssl_default(self, url):
        path_out = join(self.results_path, 'default.testssl')
        path_json = join(self.results_path, 'default_json.testssl')
        stdin, stdout, stderr = self.ssh.execute_command(f'testssl -oL {path_out} -oJ {path_json} {url}')