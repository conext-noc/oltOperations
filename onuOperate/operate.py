import os
import paramiko
import time
from dotenv import load_dotenv
from .helpers.csvParser import parser
from .activate.activate import activate
from .helpers.listChecker import compare
from .deactivate.deactivate import deactivate
from .helpers.verification import verify
load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]


def operate():
    actionList = []
    delay = 1
    action = input(
        "que accion se va a realizar? [activate | deactivate] : ")
    olt = input("en cual olt se realizara? [1|2] : ")
    ip = "181.232.180.5" if olt == "1" else "181.232.180.6"
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, port, username, password)
    comm = conn.invoke_shell()
    listType = input("se requiren datos de Odoo? [y | n] : ")
    if (listType == "y"):
        listaDeCorte = input(
            "ingrese la ruta del archivo de \"lista de corte\" (incluyendo el archivo con su archivo.extension) : ")
        listaDeClientes = input(
            "ingrese la ruta del archivo de \"lista de clientes\" (incluyendo el archivo con su archivo.extension) : ")
        list1 = parser(listaDeCorte)
        list2 = parser(listaDeClientes)
        actionList = compare(list1, list2)
    if (listType == "n"):
        listaDeClientes2 = input(
            "ingrese la ruta del archivo de \"lista de clientes\" (incluyendo el archivo con su archivo.extension) : ")
        actionList = parser(listaDeClientes2)

    def enter():
        comm.send(" \n")
        time.sleep(delay)

    def commandToSend(command):
        comm.send("{} \n".format(command))
        time.sleep(delay)

    def exitInfo():
        comm.send("Q")
        time.sleep(delay)

    if (action == "activate"):
        activate(actionList, enter, commandToSend, exitInfo, comm, olt)
        verify(actionList, action, olt)
        conn.close()
    if (action == "deactivate"):
        deactivate(actionList, enter, commandToSend, exitInfo, comm, olt)
        # verify(actionList, action, olt)
        conn.close()
    return
