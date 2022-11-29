from paramiko import SSHClient, RSAKey, AutoAddPolicy

class SecureShellSingleton(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            instace = super().__call__(*args, **kwargs)
            self._instances[self] = instace
        return self._instances[self]

class SecureShell(metaclass=SecureShellSingleton):
    def __init__(self, host, user, key_path):
        key = RSAKey.from_private_key_file(key_path)
        self.ssh = SSHClient()
        self.ssh.set_missing_host_key_policy(AutoAddPolicy())
        self.ssh.connect(hostname=host, username=user, pkey=key)

    def execute_command(self, command):
        return self.ssh.exec_command(command)

    def execute_wait_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return {'status': exit_status, 'stdin': stdin, 'stdout': stdout, 'stderr': stderr}

    def execute_commands(self, commands=[]):
        out = []
        for cmd in commands:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
            out.append({
                'cmd': cmd,
                'stdin': ssh_stdin,
                'stdout': ssh_stdout,
                'stderr': ssh_stderr,
            })
        return out

    def execute_wait_commands(self, commands=[]):
        out = []
        for cmd in commands:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
            exit_status = ssh_stdout.channel.recv_exit_status()
            out.append({
                'cmd': cmd,
                'status': exit_status,
                'stdin': ssh_stdin,
                'stdout': ssh_stdout,
                'stderr': ssh_stderr,
            })
        return out

    def close(self):
        self.ssh.close()
