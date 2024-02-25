import os
from sshtunnel import SSHTunnelForwarder

def connect(remote_ip, ssh_key_path):
	server = SSHTunnelForwarder(
		remote_ip,
		ssh_username="",
		ssh_pkey=ssh_key_path,
		remote_bind_address=("localhost", 5901),
		local_bind_address=("localhost", 5901)
	)
	server.start()
	connect_vm()
	server.stop()

def connect_vm():
	running_nt = is_windows()
	if running_nt:
		os.chdir("C:/Program Files/TigerVNC")
		os.system("vncviewer.exe localhost::5901")
	else:
		os.system("vncviewer localhost::5901")


def is_windows():
	return os.name == "nt"

