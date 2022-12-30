from utils.common.ssh import SecureShell

from os.path import join

class Gobuster:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results
        self.default_wordlist = '/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt'
        self.tech_wordlist = {
            'apache': {'extensions': [], 'wordlists': ['/usr/share/seclists/Discovery/Web-Content/ApacheTomcat.fuzz.txt', '/usr/share/seclists/Discovery/Web-Content/Apache.fuzz.txt', '/usr/share/seclists/Discovery/Web-Content/apache.txt']},
            'nginx': {'extensions': [], 'wordlists': []},
            'iis': {'extensions': [], 'wordlists': []},
        }

    def run_dir_enum(self, url, wordlist='', threads=15):
        if not wordlist:
            wordlist = self.default_wordlist
        
        path_out = join(self.results_path, 'normal_direnum.gobuster')
        out = self.ssh.execute_wait_command(f'gobuster dir -k -e -t {threads} --random-agent -o {path_out} -w {wordlist} -u {url}')
        return path_out

    def run_dir_enum_extension(self, url, wordlist, extensions, threads=15):
        if not wordlist:
            wordlist = self.default_wordlist
        
        path_out = join(self.results_path, 'extensions_direnum.gobuster')
        out = self.ssh.execute_wait_command(f'gobuster dir -k -e -t {threads} --random-agent -x {",".join(extensions)} -o {path_out} -w {wordlist} -u {url}')
        return path_out

    #TODO
    def run_dir_enum_technology(self, url, tech, threads=10):
        if tech not in self.tech_wordlist:
            raise Exception(f'[-] Technology ({tech}) not found in {self.tech_wordlist.keys()}')

    def run_vhost_enum(self, url):
        path_out = join(self.results_path, 'vhost.gobuster')
        out = self.ssh.execute_wait_command(f'gobuster vhost --append-domain -o {path_out} -w /usr/share/nmap/nselib/data/vhosts-full.lst -u {url}')
        return path_out