import paramiko
import time
import os
# import sys
from dotenv import load_dotenv
from csvParser import parser
from listChecker import compare
load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]


if __name__ == "__main__":
    def main():
        deactList = parser("LISTAS/LISTA_DE_CORTE.csv")
        clientList = parser("LISTAS/LISTA_DE_CLIENTES.csv")
        finalList = compare(deactList, clientList)
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

        def exitInfo():
            comm.send("Q")
            time.sleep(5)

        commandToSend("enable")
        enter()
        commandToSend("config")
        enter()
        for client in finalList:
            commandToSend(
                "interface gpon {}/{}".format(client["frame"], client["slot"]))
            commandToSend("ont activate {} {}".format(
                client["port"], client["id"]))
        output = comm.recv(65535)
        output = output.decode("utf-8")
        print(output)
    main()
    # print(
    #     "interface gpon {}/{}".format(client["frame"], client["slot"]))
    # print("ont deactivate {} {}".format(client["port"], client["id"]))
    # print(
    #     "interface gpon {}/{}".format(client["frame"], client["slot"]))
    # print("display ont info {} {}".format(
    #     client["port"], client["id"]))
    # main()
