from utils.common.ssh import SecureShell

from os.path import join

class WhatWeb:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def whatweb_default(self, url):
        path_out = join(self.results_path, 'default.whatweb')
        path_json = join(self.results_path, 'default_json.whatweb')
        stdin, stdout, stderr = self.ssh.execute_command(f'whatweb -a 3 --log-verbose {path_out} --log-json {path_json} {url}')

    def whatweb_aggressive(self, url):
        path_out = join(self.results_path, 'aggressive.whatweb')
        path_json = join(self.results_path, 'aggressive_json.whatweb')
        stdin, stdout, stderr = self.ssh.execute_command(f'whatweb -a 4 --log-verbose {path_out} --log-json {path_json} {url}')