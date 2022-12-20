from utils.common.ssh import SecureShell

from os.path import join

class Gobuster:
    def __init__(self):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')

    def dir_enum(self, url, path):        
        path_out = join(path, 'direnum.dirb')
        stdin, stdout, stderr = self.ssh.execute_command(f'dirb {url} -o {path_out}')

    def dir_enum_extension(self, url, path, extensions):
        path_out = join(path, 'extensions_direnum.dirb')
        ext = ','.join(map(lambda e: f'.{e}', extensions))
        stdin, stdout, stderr = self.ssh.execute_command(f'dirb {url} -X {ext} -o {path_out}')