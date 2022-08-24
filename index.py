import paramiko
import time
import os
import sys
from dotenv import load_dotenv
load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]

logs = []
logs1 = []

if __name__ == "__main__":
    def main():
        olt = input("please select OLT [1 | 2]")
        ip = "181.232.180.5" if olt == "1" else "181.232.180.6"
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(ip, port, username, password)
        comm = conn.invoke_shell()

        def enter():
            comm.send(" \n")
            time.sleep(5)

        def commandToSend(command):
            comm.send("{} \n".format(command))
            time.sleep(5)

        commandToSend("enable")
        enter()
        commandToSend("config")
        enter()
        commandToSend("display ont info by-sn 48575443BD848D48")
        enter()
        commandToSend("Q")
        enter()
        commandToSend("display ont info by-sn 4857544358C6FA3F")
        enter()
        commandToSend("Q")
        enter()
        output = comm.recv(65535)
        output = output.decode("utf-8")
        print(output)
    main()
