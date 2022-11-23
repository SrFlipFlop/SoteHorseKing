from utils.common.ssh import SecureShell

class Gobuster:
    def __init__(self):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.default_wordlist = ''
        self.tech_wordlist = {
            'apache': {'extensions': [], 'wordlist': ''},
            'nginx': {'extensions': [], 'wordlist': ''},
            'iis': {'extensions': [], 'wordlist': ''},
        }

    def dir_enum(self, url, threads):
        pass

    def dir_enum_extension(self, url, threads):
        pass

    def dir_enum_technology(self, url, threads, tech):
        if tech not in self.tech_wordlist:
            raise Exception(f'[-] Technology ({tech}) not found in {self.tech_wordlist.keys()}')