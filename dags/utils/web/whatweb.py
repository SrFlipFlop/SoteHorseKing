from utils.common.ssh import SecureShell

from os.path import join

class WhatWeb:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def run_find_technologies(self, url: str) -> str:
        path_out = join(self.results_path, 'whatweb_default.txt')
        path_json = join(self.results_path, 'whatweb_default.json')
        out = self.ssh.execute_wait_command(f'whatweb -a 3 --log-verbose {path_out} --log-json {path_json} {url}')
        return path_json

    def run_find_technologies_aggressive(self, url: str) -> str:
        path_out = join(self.results_path, 'whatweb_aggressive.txt')
        path_json = join(self.results_path, 'hatweb_aggressive.json')
        out = self.ssh.execute_wait_command(f'whatweb -a 4 --log-verbose {path_out} --log-json {path_json} {url}')
        return path_json