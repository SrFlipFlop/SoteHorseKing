from utils.common.ssh import SecureShell

from os.path import join
from urllib.parse import urlparse

class Gobuster:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results
        self.default_wordlist = '/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt'
        self.default_extensions = ['txt', 'config', 'bak']
        self.tech_wordlist = {
            'apache': {'extensions': ['php', 'phtml', 'phps', 'phpt', 'php3', 'php4', 'php5'], 'wordlists': ['/usr/share/seclists/Discovery/Web-Content/ApacheTomcat.fuzz.txt', '/usr/share/seclists/Discovery/Web-Content/Apache.fuzz.txt', '/usr/share/seclists/Discovery/Web-Content/apache.txt']},
            'nginx': {'extensions': ['js', 'php', 'py', 'java', 'rs', 'go', 'pl'], 'wordlists': ['/usr/share/seclists/Discovery/Web-Content/nginx.txt']},
            'iis': {'extensions': ['asp', 'aspx', 'asax', 'ascx', 'ashx', 'asmx', 'axd', 'dll', 'vb', 'cs'], 'wordlists': ['/usr/share/seclists/Discovery/Web-Content/iis-systemweb.txt', '/usr/share/seclists/Discovery/Web-Content/IIS.fuzz.txt']},
            'tomcat': {'extensions': ['java', 'jsp'], 'wordlists': ['/usr/share/seclists/Discovery/Web-Content/tomcat.txt']},
        }

    #Launch a basic directory enumaration using the default wordlist. Return the path of the scan result.
    def run_dir_enum(self, url: str, wordlist='', threads=15) -> str:
        if not wordlist:
            wordlist = self.default_wordlist
        
        path_out = join(self.results_path, 'gobuster_direnum.txt')
        out = self.ssh.execute_wait_command(f'gobuster dir -k -e -t {threads} --random-agent -o {path_out} -w {wordlist} -u {url}')
        return path_out

    #Launch a directory enumeration with extensions. Return the path of the scan result.
    def run_dir_enum_extension(self, url: str, extensions: list, wordlist='', threads=15) -> str:
        if not wordlist:
            wordlist = self.default_wordlist
        
        path_out = join(self.results_path, 'gobuster_extensions_direnum.txt')
        out = self.ssh.execute_wait_command(f'gobuster dir -k -e -t {threads} --random-agent -x {",".join(extensions)} -o {path_out} -w {wordlist} -u {url}')
        return path_out

    #Launch a directory enumeration based on the technology using different wordlists and extensions. Return the path of the scan result.
    def run_dir_enum_technology(self, url: str, tech: str, threads=10)  -> str:
        if tech.lower() not in self.tech_wordlist:
            raise Exception(f'[-] Technology ({tech}) not found in {self.tech_wordlist.keys()}')

        domain = url
        if 'http' in domain:
            domain = urlparse(domain).netloc

        path_out = join(self.results_path, 'gobuster_tech_direnum.txt')
        extensions = ','.join(self.tech_wordlist[tech.lower()]['extensions'] + self.default_extensions)
        wordlist = ' '.join(self.tech_wordlist[tech.lower()]['wordlist'])
        commands = (
            f'cat {wordlist} > /tmp/gobuster_tech_{domain}.txt',
            f'gobuster dir -k -e -t {threads} --random-agent -x {extensions} -o {path_out} -w / -u {url}',
            f'rm /tmp/gobuster_tech_{domain}.txt'
        )
        out = self.ssh.execute_wait_commands(commands)
        return path_out
        
    #Launch an vhost bruteforce enumeration. Return the path of the scan result.
    def run_vhost_enum(self, url: str) -> str:
        path_out = join(self.results_path, 'gobuster_vhostenum.txt')
        out = self.ssh.execute_wait_command(f'gobuster vhost --append-domain -o {path_out} -w /usr/share/nmap/nselib/data/vhosts-full.lst -u {url}')
        return path_out

    #TODO
    def analyze_sensitive_directories(self, path: str) -> None:
        pass