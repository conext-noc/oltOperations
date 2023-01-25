import os
from time import sleep
import paramiko
from dotenv import load_dotenv

load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]


def ssh(ip, debugging):
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
        if debugging:
            print(f"""
{cmd}
                """)
        enter()

    def quit():
        conn.close()

    if ip == "181.232.180.5" or ip == "181.232.180.6" or ip == "181.232.180.7":
        command("enable")
        command("config")
        command("scroll 512")
    else:
        command("sys")

    return (comm, command, quit)
