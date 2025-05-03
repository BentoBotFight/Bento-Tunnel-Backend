import paramiko
import time
command = "comfy i2c-dc 1 1"

# Update the next three lines with your
# server's information

# This is my default PiTunnel host, replace it with your own
host = "us2.pitunnel.net"
username = "comfy"
password = "comfy"
port = 22156

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password, port = port)
_stdin, _stdout,_stderr = client.exec_command("comfy i2c-dc 1 0")
print(_stdout.read().decode())
client.close()