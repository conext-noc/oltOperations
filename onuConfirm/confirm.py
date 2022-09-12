import time
from dotenv import load_dotenv
import os
import paramiko
from onuConfirm.helpers.spidInfo import getSPID
from onuConfirm.helpers.onuIdInfo import addONU, addOnuService
from onuConfirm.helpers.ontCheck import verifyValues
load_dotenv()

username = os.environ["user"]
password = os.environ["password"]
port = os.environ["port"]

providerMap = {
    "inter": 1101,
    "vnet": 1102
}

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power(dBm)                  : "


def confirm():
    delay = 1
    olt = input("Select OLT [1|2] : ")
    ip = "181.232.180.5" if olt == "1" else "181.232.180.6"
    isNew = input("will you add a new client? [y|n] : ")
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, port, username, password)
    comm = conn.invoke_shell()

    def enter():
        comm.send(" \n")
        time.sleep(delay)

    def commandToSend(command):
        comm.send("{} \n".format(command))
        time.sleep(delay)

    if (isNew == "y"):
        clientSlot = input("enter client slot : ")
        clientPort = input("enter client port : ")
        clientName = input("enter the ont client name : ")
        clientProvider = input("enter client Provider [inter | vnet] : ")
        clientSN = input("enter client serial : ")
        clientPlan = input("enter the client's data plan : ")
        deviceType = input("enter the client ONU type : ")

        spid = getSPID(comm, delay, commandToSend, enter)
        ontId = addONU(comm, clientSN, clientSlot, clientPort,
                       clientProvider, clientName, deviceType, commandToSend, enter)
        (temp, pwr) = verifyValues(comm, clientSlot,
                                   clientPort, ontId, commandToSend, enter)
        proceed = input(
            f"ONT power is {pwr} and Temperature is {temp} do you want to proceed? [y|n] : ")
        if (proceed == "y"):
            addOnuService(comm, spid, clientProvider,
                          clientSlot, clientPort, ontId, clientPlan, commandToSend, enter)
            print(
                f"""{clientName} 0/{clientSlot}/{clientPort}/{ontId} OLT {olt} {clientProvider.upper()} {clientPlan[3:]} \nTEMPERATURA: {temp} \nPOTENCIA: {pwr}""")
            os.remove("ResultSPID.txt")
            os.remove("ResultONTID.txt")
            os.remove("ResultPwr.txt")
            os.remove("ResultTemp.txt")
            conn.close()
            return
        if (proceed == "n"):
            reason = input("why the ont wont have service? : ")
            print(
                f"""\n{clientName} 0/{clientSlot}/{clientPort}/{ontId} OLT {olt} {clientProvider.upper()} {clientPlan[3:]} \nTEMPERATURA: {temp} \nPOTENCIA: {pwr} \n- {reason} - \nSPID : {spid}""")
            os.remove("ResultSPID.txt")
            os.remove("ResultONTID.txt")
            os.remove("ResultPwr.txt")
            os.remove("ResultTemp.txt")
            conn.close()
            return
    if (isNew == "n"):
        spid = getSPID(comm, delay, commandToSend, enter)
        spid = input("enter the corresponding service port virtual id")
        clientSlot = input("enter client slot : ")
        clientPort = input("enter client port : ")
        clientONUID = input("enter client onu id : ")
        clientName = input("enter client name : ")
        clientProvider = input("enter client Provider [inter | vnet] : ")
        clientPlan = input("enter the client's data plan : ")

        (temp, pwr) = verifyValues(comm, clientSlot,
                                   clientPort, clientONUID, commandToSend, enter)
        proceed = input(
            f"ONT power is {pwr} and Temperature is {temp} do you want to proceed? [y|n] : ")
        if (proceed == "y"):
            addOnuService(comm, spid, clientProvider,
                          clientSlot, clientPort, clientONUID, clientPlan, commandToSend, enter)
            print(
                f"""{clientName} 0/{clientSlot}/{clientPort}/{clientONUID} OLT {olt} {clientProvider.upper()} {clientPlan[3:]} \nTEMPERATURA: {temp} \nPOTENCIA: {pwr}""")
            os.remove("ResultPwr.txt")
            os.remove("ResultTemp.txt")
            conn.close()
            return
        if (proceed == "n"):
            reason = input("why the ont wont have service? : ")
            print(
                f"""{clientName} 0/{clientSlot}/{clientPort}/{ontId} OLT {olt} {clientProvider.upper()} {clientPlan[3:]} \nTEMPERATURA: {temp} \nPOTENCIA: {pwr} \n- {reason} -\nSPID : {spid}""")
            os.remove("ResultPwr.txt")
            os.remove("ResultTemp.txt")
            conn.close()
            return
