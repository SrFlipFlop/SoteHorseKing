from utils.common.ssh import SecureShell

from re import findall
from os.path import join
from json import dump

class Nmap:
    def __init__(self, connect=True):
        if connect:
            self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.common_web_ports = ['66', '80', '81', '443', '445', '457', '1080', '1100', '1241', '1352', '1433', '1434', '1521', '1944', '2301', '3000', '3128', '3306', '4000', '4001', '4002', '4100', '5000', '5432', '5800', '5801', '5802', '6346', '6347', '7001', '7002', '8000', '8080', '8181', '8443', '8888', '30821']

    def find_web_servers(self, host, ports, path):
        if not ports:
            ports = ', '.join(self.common_web_ports)

        path_normal = join(path, 'find_web_servers.nmap')
        out = self.ssh.execute_wait_command(f'nmap -sT -sV -oN {path_normal} -oG - -p {ports} {host}')

        #Find results (TODO: parse results from stdout and grep for services)
        lines = out['stdout'].readlines()
        results = findall(r'([0-9]+)/open/tcp/', 'test')
        results = {}
        if results:
            with open(join(path, 'find_web_servers.results'), 'w') as f:
                dump(f, results)

    def nmap_web_scripts(self, host, ports):
        pass
