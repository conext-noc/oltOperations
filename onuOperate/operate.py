import os
import paramiko
import time
from dotenv import load_dotenv
from .helpers.csvParser import parser
from .activate.activate import activate
# from .helpers.listChecker import compare
from .deactivate.deactivate import deactivate
# from .helpers.verification import verify
load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]


def operate():
    delay = 1
    action = input(
        "Which action will be performed? [activate | deactivate] : ")
    olt = input("In Which OLT the action will be performed? [1|2] : ")
    ip = "181.232.180.5" if olt == "1" else "181.232.180.6"
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, port, username, password)
    comm = conn.invoke_shell()
    # actList = input("is a small lot? [yes | no] : ")
    # list1 = parser("onuOperate/LISTAS/LISTA_DE_CORTE.csv")
    # list2 = parser("onuOperate/LISTAS/LISTA_DE_CLIENTES.csv")
    # actionList1 = compare(list1, list2)
    actionList = parser(
        "onuOperate/LISTAS/OLT1.csv") if olt == "1" else parser("onuOperate/LISTAS/OLT2.csv")
    # actionList = actionList2 if actList == "yes" else actionList1

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
        # verify(actionList, action, olt)
        conn.close()
    if (action == "deactivate"):
        deactivate(actionList, enter, commandToSend, exitInfo, comm, olt)
        # verify(actionList, action, olt)
        conn.close()
    return
