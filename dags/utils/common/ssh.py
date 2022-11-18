from paramiko import SSHClient, RSAKey, AutoAddPolicy

class SecureShellSingleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            instace = super().__call__(*args, **kwargs)
            self._instances[self] = instace
        return self._instances[self]

#TODO: class singleton?
class SecureShell(metaclass=SecureShellSingleton):
    def __init__(self, host, user, key_path):
        key = RSAKey.from_private_key_file(key_path) #/opt/airflow/config/id_rsa
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(hostname=host, username=user, pkey=key)

    def execute(self, commands=[]):
        for cmd in commands:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
