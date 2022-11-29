from utils.common.ssh import SecureShell

from os.path import join

class Gobuster:
    def __init__(self):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')

    def vhost_enum(self, domain, path):
        path_out = join(path, 'vhost.gobuster')
        commands = (
            f'sed "s/$/.{domain}/" /usr/share/nmap/nselib/data/vhosts-full.lst > /tmp/vhost_domains_{domain}.txt'
            f'vhosts-sieve -d /tmp/vhost_domains_{domain}.txt -o {path_out}',
            f'rm /tmp/vhost_domains_{domain}.txt'
        )
        out = self.ssh.execute_wait_commands(commands)