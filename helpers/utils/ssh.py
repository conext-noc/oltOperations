import os
from time import sleep
import paramiko
from dotenv import load_dotenv

from helpers.utils.sheets import get_creds
from helpers.utils.printer import colorFormatter, log

load_dotenv()



def ssh(ip, debugging):
    count = 1
    delay = 1.5
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    comm = None
    cont = True
    creds = get_creds()

    # Handling multiple SSH sessions
    while cont and count <= 3:
        try:
            username = creds[count - 1][f"user_{count}"]
            password = creds[count - 1][f"password_{count}"]
            port = 22
            conn.connect(ip, port, username, password)
            comm = conn.invoke_shell()
            cont = False
        except paramiko.ssh_exception.AuthenticationException:
            cont = True
            count += 1
            continue
        break
    
    def enter():
        comm.send(" \n")
        comm.send(" \n")
        sleep(delay)

    def command(cmd):
        comm.send(cmd)
        sleep(delay)
        if debugging:
            log(colorFormatter(f"""
{cmd}""","info"))
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
