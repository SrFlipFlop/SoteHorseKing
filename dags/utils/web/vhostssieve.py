from utils.common.ssh import SecureShell

from os.path import join
from urllib.parse import urlparse

class VhostSieve:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #Create a temporal wordlist using the domain and launch the vhost-sieve. Return the path of the output.
    def run_vhost_enum(self, domain: str) -> str:
        if 'http' in domain:
            domain = urlparse(domain).netloc

        path_out = join(self.results_path, 'vhostsieve.txt')
        commands = (
            f'sed "s/$/.{domain}/" /usr/share/nmap/nselib/data/vhosts-full.lst > /tmp/vhost_domains_{domain}.txt',
            f'vhosts-sieve -d /tmp/vhost_domains_{domain}.txt -o {path_out}',
            f'rm /tmp/vhost_domains_{domain}.txt'
        )
        out = self.ssh.execute_wait_commands(commands)
        return path_out