from utils.common.ssh import SecureShell

from os.path import join

class Gobuster:
    def __init__(self):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.default_wordlist = '/usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt'
        self.tech_wordlist = {
            'apache': {'extensions': [], 'wordlists': ['/usr/share/seclists/Discovery/Web-Content/ApacheTomcat.fuzz.txt', '/usr/share/seclists/Discovery/Web-Content/Apache.fuzz.txt', '/usr/share/seclists/Discovery/Web-Content/apache.txt']},
            'nginx': {'extensions': [], 'wordlists': []},
            'iis': {'extensions': [], 'wordlists': []},
        }

    def dir_enum(self, url, wordlist, path, threads=15):
        if not wordlist:
            wordlist = self.default_wordlist
        
        path_out = join(path, 'normal_direnum.gobuster')
        stdin, stdout, stderr = self.ssh.execute_command(f'gobuster dir -k -e -t {threads} --random-agent -o {path_out} -w {wordlist} -u {url}')

    def dir_enum_extension(self, url, wordlist, path, extensions, threads=15):
        if not wordlist:
            wordlist = self.default_wordlist
        
        path_out = join(path, 'extensions_direnum.gobuster')
        stdin, stdout, stderr = self.ssh.execute_command(f'gobuster dir -k -e -t {threads} --random-agent -x {",".join(extensions)} -o {path_out} -w {wordlist} -u {url}')

    #TODO
    def dir_enum_technology(self, url, path, tech, threads=10):
        if tech not in self.tech_wordlist:
            raise Exception(f'[-] Technology ({tech}) not found in {self.tech_wordlist.keys()}')

    def vhost_enum(self, url, path):
        path_out = join(path, 'vhost.gobuster')
        stdin, stdout, stderr = self.ssh.execute_command(f'gobuster vhost --append-domain -o {path_out} -w /usr/share/nmap/nselib/data/vhosts-full.lst -u {url}')