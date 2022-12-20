from utils.common.ssh import SecureShell

from os.path import join

class Nuclei:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def nuclei_default(self, url):
        path_out = join(self.results_path, 'default.nuclei')
        stdin, stdout, stderr = self.ssh.execute_command(f'nuclei -fr -o {path_out} -u {url}')

    #TODO
    def nuclei_new_templates(self, url):
        path_out = join(self.results_path, 'new.nuclei')
        stdin, stdout, stderr = self.ssh.execute_command(f'nuclei -nt -fr -o {path_out} -u {url}')
    
    #TODO
    def nuclei_cve(self, url):
        path_out = join(self.results_path, 'vulnerabilities.nuclei')
        stdin, stdout, stderr = self.ssh.execute_command(f'nuclei -t cves -t vulnerabilities -fr -o {path_out} -u {url}')