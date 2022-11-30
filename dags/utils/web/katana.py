from utils.common.ssh import SecureShell

from os.path import join

class Katana:
    def __init__(self):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')

    def crawl_full(self, url, path):
        path_out = join(path, 'full-crawler-depth5.katana')
        out = self.ssh.execute_wait_command(f'katana -d 5 -jc -kf all -o {path_out} -u {url}')
        return ''.join(map(str, out['stdout'].readlines()))

    #TODO
    def analyze_lfi(self, data):
        pass

    #TODO
    def analyze_redirects(self, data):
        pass

    #TODO
    def analyze_idor(self, data):
        pass