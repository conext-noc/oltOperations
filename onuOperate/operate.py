import os
import tkinter as tk
from tkinter import filedialog
import paramiko
import time
from dotenv import load_dotenv
from .helpers.csvParser import parser
from .activate.activate import activate
from .helpers.listChecker import compare
from .deactivate.deactivate import deactivate
from .helpers.verification import verify, verifyODOO
load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]
root = tk.Tk()
root.withdraw()

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
    print("ingrese la ruta de destino para los resultados de la operacion")
    time.sleep(2)
    result_path = filedialog.askdirectory()

    if (listType == "y"):
        print("ingrese la ruta del archivo de \"lista de corte\"")
        time.sleep(2)
        listaDeCorte = filedialog.askopenfilename()
        print("ingrese la ruta del archivo de \"lista de clientes\"")
        time.sleep(2)
        listaDeClientes = filedialog.askopenfilename()
        list1 = parser(listaDeCorte)
        list2 = parser(listaDeClientes)
        actionList = compare(list1, list2)

    if (listType == "n"):
        print("ingrese la ruta del archivo de \"lista de clientes\"")
        time.sleep(2)
        listaDeClientes2 = filedialog.askopenfilename()
        actionList = parser(listaDeClientes2)

    def enter():
        comm.send(" \n")
        time.sleep(delay)

    def commandToSend(command):
        comm.send("{} \n".format(command))
        time.sleep(delay)

    commandToSend("enable")
    commandToSend("config")
    outputX = comm.recv(65535)
    outputX = outputX.decode("ascii")

    activate(actionList, enter, commandToSend, comm, olt) if action == "activate" else (deactivate(actionList, enter, commandToSend, comm, olt) if action == "deactivate" else None)
    verify(actionList, action, olt,result_path) if listType == "n" else verifyODOO(actionList, action, olt,result_path)
    conn.close()
    return
