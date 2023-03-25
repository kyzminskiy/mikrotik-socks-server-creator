import paramiko
import secrets
import string
import random
from config import *


def generate_socks_port():
    """Generates a random port number."""
    return random.randint(socks_port_range[0], socks_port_range[1])


def generate_socks_username():
    """Generates a random username."""
    return ''.join(secrets.choice(string.ascii_letters) for i in range(username_length))


def generate_socks_password():
    """Generates a random password."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(password_length))


with open(ssh_access_file, 'r') as f:
    for line in f:
        ssh_access = line.strip().split(':')
        ssh_host, ssh_username, ssh_password = ssh_access[0], ssh_access[1], ssh_access[2]
        socks_port, socks_username, socks_password = generate_socks_port(), generate_socks_username(), generate_socks_password()

        # SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ssh_host, port=22, username=ssh_username, password=ssh_password)

        # Create a new SOCKS server
        ssh.exec_command(f"/ip socks set enabled=yes port={socks_port} version={socks_version}" + ' auth-method=password' if socks_auth else '')
        if delete_all_previous_socks_users:
            ssh.exec_command("/ip socks users remove [find]")
        if socks_auth:
            ssh.exec_command(f"/ip socks users add name={socks_username} password={socks_password}")

        with open(socks_create_file, 'a') as f:
            f.write(f"{ssh_host}:{socks_port}:{socks_username}:{socks_password}\n")
            print(f"{ssh_host}:{socks_port}:{socks_username}:{socks_password}")

        # Close the SSH connection
        ssh.close()