from utils.common.ssh import SecureShell

from json import dump
from re import findall
from os.path import join
from urllib.parse import urlparse

class Nmap:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results
        self.default_web_ports = ['80', '443', '8080', '8443']
        self.common_web_ports = [
            '66',
            '80',
            '81',
            '443',
            '445',
            '457',
            '1080',
            '1100',
            '1241',
            '1352',
            '1433',
            '1434',
            '1521',
            '1944',
            '2301',
            '3000',
            '3128',
            '3306',
            '4000',
            '4001',
            '4002',
            '4100',
            '5000',
            '5432',
            '5800',
            '5801',
            '5802',
            '6346',
            '6347',
            '7001',
            '7002',
            '8000',
            '8080',
            '8181',
            '8443',
            '8888',
            '30821'
        ]
        self.web_scripts = [
            'http-adobe-coldfusion-apsa1301.nse',
            'http-apache-server-status.nse',
            'http-aspnet-debug.nse',
            'http-bigip-cookie.nse',
            'http-cakephp-version.nse',
            'http-cisco-anyconnect.nse',
            'http-coldfusion-subzero.nse',
            'http-cors.nse',
            'http-frontpage-login.nse',
            'http-headers.nse',
            'http-iis-webdav-vuln.nse',
            'http-internal-ip-disclosure.nse',
            'http-litespeed-sourcecode-download.nse',
            'http-majordomo2-dir-traversal.nse',
            'http-mcmp.nse',
            'http-methods.nse',
            'http-ntlm-info.nse',
            'http-php-version.nse',
            'http-robots.txt.nse',
            'http-shellshock.nse',
            'http-trace.nse',
            'http-vmware-path-vuln.nse',
            'http-vuln-cve2006-3392.nse',
            'http-vuln-cve2009-3960.nse',
            'http-vuln-cve2010-0738.nse',
            'http-vuln-cve2010-2861.nse',
            'http-vuln-cve2011-3192.nse',
            'http-vuln-cve2011-3368.nse',
            'http-vuln-cve2012-1823.nse',
            'http-vuln-cve2013-0156.nse',
            'http-vuln-cve2013-6786.nse',
            'http-vuln-cve2013-7091.nse',
            'http-vuln-cve2014-2126.nse',
            'http-vuln-cve2014-2127.nse',
            'http-vuln-cve2014-2128.nse',
            'http-vuln-cve2014-2129.nse',
            'http-vuln-cve2014-3704.nse',
            'http-vuln-cve2014-8877.nse',
            'http-vuln-cve2015-1427.nse',
            'http-vuln-cve2015-1635.nse',
            'http-vuln-cve2017-1001000.nse',
            'http-vuln-cve2017-5638.nse',
            'http-vuln-cve2017-5689.nse',
            'http-vuln-cve2017-8917.nse',
            'http-waf-detect.nse',
            'http-waf-fingerprint.nse',
            'http-webdav-scan.nse'
        ]

    #Run fast nmap for default ports. Return the path of the results
    def run_web_fast(self, host: str, ports=[]) -> dict:
        host = self._clean_host(host)
        if ports:
            scan_ports = ','.join(map(lambda x: str(x), ports))
        else:
            scan_ports = ','.join(self.common_web_ports)

        normal_result = join(self.results_path, 'nmap_web_fast.txt')
        grep_results = join(self.results_path, 'nmap_web_fast.gnmap')
        out = self.ssh.execute_wait_command(f'nmap -sT -sV -T4 -oN {normal_result} -oG {grep_results} -p {scan_ports} {host}')
        print(f'[+] Execudet web_fast - {out} - {normal_result} - {grep_results}')
        return {'gnmap': grep_results, 'nmap': normal_result}

    #Run slow nmap with multiple scripts. Return the path of the result
    def run_web_scripts(self, host: str, ports=[]) -> dict:
        host = self._clean_host(host)
        if ports:
            scan_ports = ','.join(map(lambda x: str(x), ports))
        else:
            scan_ports = ','.join(self.default_web_ports)

        normal_result = join(self.results_path, 'nmap_web_scripts.txt')
        out = self.ssh.execute_wait_command(f'nmap -sT -sV --script {",".join(self.web_scripts)} -oN {normal_result} -p {scan_ports} {host}')
        return {'nmap': normal_result}

    #Analyze the gnmap file to find open web applications in different ports
    def analyze_webservers(self, gnmap_path: str) -> None:
        with open(gnmap_path, 'r') as f:
            gnmap = f.read()

        res1 = findall(r'Host: ([0-9a-zA-Z_\s\-\.]+) \(([0-9a-zA-Z_\s\-\.]+)?\)\sPorts:', gnmap)
        res2 = findall(r'([0-9]+)/open/tcp//http([0-9a-zA-Z_\s\-\.\(\)]+)?//([0-9a-zA-Z_\s\-\.\(\)]+)/', gnmap)
        
        if res1 and res2:
            host = res1[0][0]
            webs = ''.join([f'{host}:{x[0]} [{x[2]}]\n' for x in res2])
            results = {
                'tpye': 'recon',
                'module': 'web_servers',
                'description': 'Find alternative web servers on the target machine. These alternative web servers could run old versions or a pre-production environment with new vulnerabilities or sensitive information.',
                'risk': 'INFORMATIVE',
                'cvss': 0,
                'result': f'It has been found the following HTTP servers in the remote host:\n{webs}',
            }

            with open(join(self.results_path, 'web_servers.results'), 'w') as f:
                dump(results, f)        
    
    def _clean_host(self, host: str) -> str:
        if 'http' in host:
            host = urlparse(host).netloc
        if ':' in host:
            host = host.split(':')[0]
        return host