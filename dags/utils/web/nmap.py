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
        out = self.ssh.execute_wait_command(f'nmap -sT -sV -T4 -oN {path_normal} -oG - -p {ports} {host}')
        
        nmap_out = ' '.join(map(str, out['stdout'].readlines()))
        open_ports = findall(r'([0-9]+)/open/tcp//http?[0-9a-zA-Z-_]+/', nmap_out)
        
        if open_ports:
            ports_string = ''.join([f'- {host}:{p}\n' for p in open_ports])
            results = {
                'tpye': 'recon',
                'module': 'find_web_servers',
                'description': 'Find alternative web servers on the target machine. These alternative web servers could run old versions or a pre-production environment with new vulnerabilities or sensitive information.',
                'risk': 'INFORMATIVE',
                'cvss': 0,
                'result': f'It has been found the following HTTP servers in the remote host:\n{ports_string}',
            }
            self.store_results(path, 'find_web_servers.results', results)
            
    def nmap_web_scripts(self, host, ports):
        pass

    def store_results(self, path, file, results):
        with open(join(path, file), 'w') as f:
            dump(results, f)
