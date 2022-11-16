import os
from time import sleep
import paramiko
from dotenv import load_dotenv

load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]


def ssh(ip):
    delay = 1.5
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, port, username, password)
    comm = conn.invoke_shell()

    def enter():
        comm.send(" \n")
        comm.send(" \n")
        sleep(delay)

    def command(cmd):
        comm.send(cmd)
        sleep(delay)
        enter()

    def close():
        conn.close()

    return (comm, command, close)
