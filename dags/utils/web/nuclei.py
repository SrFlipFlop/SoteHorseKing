from utils.common.ssh import SecureShell

from os.path import join

class Nuclei:
    def __init__(self, results: str) -> None:
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    #Launch the default nuclei scan. Return the results path
    def run_nuclei_default(self, url: str) -> str:
        path_out = join(self.results_pgiath, 'nuclei_default.txt')
        out = self.ssh.execute_wait_command(f'nuclei -fr -o {path_out} -u {url}')
        return path_out

    #Launch a nuclei scan only using new templates. Return the results path
    def run_nuclei_new_templates(self, url: str) -> str:
        path_out = join(self.results_path, 'nuclei_new_templates.txt')
        out = self.ssh.execute_wait_command(f'nuclei -nt -fr -o {path_out} -u {url}')
        return path_out

    #Launch a nuclei scan only for vulnerabilities and CVE templates. Return the results path
    def run_nuclei_cve(self, url: str) -> str:
        path_out = join(self.results_path, 'nuclei_vulnerabilities.txt')
        out = self.ssh.execute_wait_command(f'nuclei -t cves -t vulnerabilities -fr -o {path_out} -u {url}')
        return path_out