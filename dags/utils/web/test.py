from utils.common.ssh import SecureShell

class Test:
    def __init__(self):
        self.var = 'Test'

    def test(self):
        ssh = SecureShell('web-tools', 'root', '/opt/airflow/config/id_rsa')
        print(id(ssh))
        ssh.execute_command('sleep 30')
