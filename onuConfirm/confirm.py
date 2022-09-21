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
p = os.environ["port"]

providerMap = {
    "inter": 1101,
    "vnet": 1102
}

conditionTemp = "Temperature\(C\)                         : "
conditionPwr = "Rx optical power(dBm)                  : "


def confirm():
    delay = 1
    olt = input("Seleciona la OLT [1|2] : ")
    ip = "181.232.180.5" if olt == "1" else "181.232.180.6"
    isNew = input("se agregara un cliente nuevo? [y|n] : ")
    conn = paramiko.SSHClient()
    conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conn.connect(ip, p, username, password)
    comm = conn.invoke_shell()

    def enter():
        comm.send("\n")
        time.sleep(delay)

    def commandToSend(command):
        comm.send(f"{command}")
        time.sleep(delay)

    commandToSend("enable")
    enter()
    commandToSend("config")
    enter()

    if (isNew == "y"):
        slot = input("ingrese slot de cliente : ")
        port = input("ingrese puerto de cliente : ")
        name = input("ingrese nombre del cliente : ")
        provider = input(
            "ingrese proevedor de cliente [inter | vnet] : ")
        sn = input("ingrese serial de cliente : ")
        plan = input("ingrese plan de cliente : ")
        deviceType = input("ingrese tipo de ont de cliente : ")

        spid = getSPID(comm, commandToSend, enter)
        ontId = addONU(comm, sn, slot, port, providerMap[provider], name, deviceType, commandToSend, enter)
        (temp, pwr) = verifyValues(comm, slot, port, ontId, commandToSend, enter)
        proceed = input(f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [y|n] : ")
        if (proceed == "y"):
            addOnuService(spid, providerMap[provider], slot, port, ontId, plan, commandToSend, enter, comm)
            os.remove("ResultSPID.txt")
            os.remove("ResultONTID.txt")
            os.remove("ResultPwr.txt")
            os.remove("ResultTemp.txt")
            conn.close()
            return
        if (proceed == "n"):
            reason = input("por que no se le asignara servicio? : ")
            print(f"""{name} 0/{slot}/{port}/{ontId} OLT {olt} {provider.upper()} {plan[3:]}\nTEMPERATURA:{temp}\nPOTENCIA:{pwr}\nSPID :{spid}\n - {reason} -""")
            os.remove("ResultSPID.txt")
            os.remove("ResultONTID.txt")
            os.remove("ResultPwr.txt")
            os.remove("ResultTemp.txt")
            conn.close()
            return
    if (isNew == "n"):
        slot = input("ingrese slot de cliente : ")
        port = input("ingrese puerto de cliente : ")
        clientONUID = input("enter client ont id : ")
        name = input("enter client name : ")
        provider = input("enter client Provider [inter | vnet] : ")
        spid = input("enter the corresponding service port virtual id : ")
        plan = input("ingrese plan de cliente : ")

        (temp, pwr) = verifyValues(comm, slot, port, clientONUID, commandToSend, enter)
        proceed = input(f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [y|n] : ")
        if (proceed == "y"):
            addOnuService(spid, providerMap[provider], slot, port, clientONUID, plan, commandToSend, enter)
            print(f"""{name} 0/{slot}/{port}/{ontId} OLT {olt} {provider.upper()} {plan[3:]}\nTEMPERATURA:{temp}\nPOTENCIA:{pwr}\nSPID :{spid}""")
            os.remove("ResultPwr.txt")
            os.remove("ResultTemp.txt")
            conn.close()
            return
        if (proceed == "n"):
            reason = input("por que no se le asignara servicio? : ")
            print(f"""{name} 0/{slot}/{port}/{ontId} OLT {olt} {provider.upper()} {plan[3:]}\nTEMPERATURA:{temp}\nPOTENCIA:{pwr}\nSPID :{spid}\n - {reason} -""")
            os.remove("ResultPwr.txt")
            os.remove("ResultTemp.txt")
            conn.close()
            return
