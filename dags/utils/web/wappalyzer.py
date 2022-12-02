from utils.common.ssh import SecureShell

from os.path import join
from json import loads, dump

class Wappalyzer:
    def __init__(self, results):
        self.ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        self.results_path = results

    def find_technologies(self, url):
        path_out = join(self.results_path, 'technologies.wappy')
        out = self.ssh.execute_wait_command(f'wappy -j -kbc {url} | tee {path_out}')
        return loads(''.join(map(str, out['stdout'].readlines())))
        
    def analyze_technologies(self, out):
        technologies = []
        lines = []
        for tech in out:
            technologies.append(tech['name'])
            lines.append(f'- {tech["name"]} {"-" if tech["version"] else ""} {tech.get("version", "")} ({", ".join(tech["categories"])})\n')

        results = {
            'tpye': 'recon',
            'module': 'find_technologies',
            'description': 'Find the technologies used by the web application. These information could be used to perform advanced attacks using the server technologies.',
            'risk': 'INFORMATIVE',
            'cvss': 0,
            'result': f'It has been found the following technologies in the remote host:\n{"".join(lines)}',
        }
        with open(join(self.results_path, 'technologies.results'), 'w') as f:
            dump(results, f)
        
        return technologies