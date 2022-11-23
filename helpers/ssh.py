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

    def quit(d):
        conn.close()
        sleep(d)

    if ip == "181.232.180.5" or ip == "181.232.180.6" or ip == "181.232.180.7":
        command("enable")
        command("config")

    return (comm, command, quit)
