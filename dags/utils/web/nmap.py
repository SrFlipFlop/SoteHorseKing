from utils.common.ssh import SecureShell

from re import findall
from os.path import join
from json import dump

class Nmap:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results
        self.default_web_ports = ['80', '443', '8080', '8443']
        self.common_web_ports = ['66', '80', '81', '443', '445', '457', '1080', '1100', '1241', '1352', '1433', '1434', '1521', '1944', '2301', '3000', '3128', '3306', '4000', '4001', '4002', '4100', '5000', '5432', '5800', '5801', '5802', '6346', '6347', '7001', '7002', '8000', '8080', '8181', '8443', '8888', '30821']
        self.web_scripts = []

    def nmap_web_fast(self, host, ports):
        if ports:
            scan_ports = ','.join(ports)
        else:
            scan_ports = ','.join(self.common_web_ports)

        normal_result = join(self.results_path, 'find_web_servers.nmap')
        out = self.ssh.execute_wait_command(f'nmap -sT -sV -T4 -oN {normal_result} -oG - -p {scan_ports} {host}')
        return ' '.join(map(str, out['stdout'].readlines()))

    #TODO: filter http scripts   
    def nmap_web_scripts(self, host, ports):
        if not ports:
            ports = ','.join(self.default_web_ports)

        normal_result = join(self.results_path, 'nmap_web_scripts.nmap')
        stdin, stdout, stderr = self.ssh.execute_command(f'nmap -sT -sV --script {",".join(self.web_scripts)} -oN {normal_result} -p {ports} {host}')

    #TODO: generate good report for open web servers
    def analyze_webservers(self, gnmap):
        open_ports = findall(r'([0-9]+)/open/tcp//http?[0-9a-zA-Z-_]+/', gnmap)
        
        host = "localhost"
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
            
            with open(join(self.results_path, 'find_web_servers.results'), 'w') as f:
                dump(results, f)        
    