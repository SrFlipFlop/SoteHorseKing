from utils.common.ssh import SecureShell

from os.path import join

class WPScan:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results
        self.users_wordlist = '/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt'
        self.passwords_wordlist = '/usr/share/seclists/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt'

    def wpscan_default(self, url):
        path_out = join(self.results_path, 'wpscan_default.json')
        stdin, stdout, stderr = self.ssh.execute_command(f'wpscan --url {url} --rua -o {path_out} -f json')

    def wpscan_aggressive(self, url, threads=10):
        path_out = join(self.results_path, 'wpscan_aggressive.json')
        stdin, stdout, stderr = self.ssh.execute_command(f'wpscan --url {url} --rua --disable-tls-checks -o {path_out} -f json -t {threads} -e ap,at,tt,cb,dbe,u,m --detection-mode aggressive --plugins-detection aggressive --plugins-version-detection aggressive')

    def wpscan_password(self, url, usernames, passwords, threads=20):
        if not usernames:
            usernames = self.users_wordlist
        if not passwords:
            passwords = self.passwords_wordlist
        
        path_out = join(self.results_path, 'wpscan_password.json')
        stdin, stdout, stderr = self.ssh.execute_command(f'wpscan --url {url} -o {path_out} -f json -t {threads} --stealthy -U {usernames} -P {passwords}')