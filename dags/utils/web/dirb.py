from utils.common.ssh import SecureShell

from os.path import join

class Dirb:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #Launch a basic directory enumaration using dirb default wordlist. Return the path of the scan result.
    def run_dir_enum(self, url: str) -> str:
        path_out = join(self.results_path, 'dirb_direnum.txt')
        out = self.ssh.execute_wait_command(f'dirb {url} -o {path_out}')
        return path_out

    #Launch a directory enumeration with extensions. Return the path of the scan result.
    def run_dir_enum_extension(self, url: str, extensions: list) -> str:
        path_out = join(self.results_path, 'dirb_extensions_direnum.txt')
        ext = ','.join(map(lambda e: f'.{e}', extensions))
        out= self.ssh.execute_wait_command(f'dirb {url} -X {ext} -o {path_out}')
        return path_out