from helpers.outputDecoder import parser, check
from helpers.ontCheck import verifyValues
from helpers.getWanData import wan
from time import sleep

from helpers.serialLookup import serialSearch

existingCond = (
    "-----------------------------------------------------------------------------"
)
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "
existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
}


def newLookup(comm, command, olt):
    client = []
    command("display ont autofind all | no-more")
    sleep(5)
    (value, regex) = parser(comm, newCond, "m")
    for ont in range(len(regex) - 1):
        (_, s) = regex[ont]
        (e, _) = regex[ont + 1]
        result = value[s:e]
        (_, eFSP) = check(result, newCondFSP).span()
        (_, eSN) = check(result, newCondSn).span()
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[eFSP : eFSP + 6].replace("\n", "").replace(" ", "")
        client.append({"FSP": aFSP, "SN": aSN, "IDX": ont})
    print("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "SN"))
    for ont in client:
        FSP = ont["FSP"].replace(" ", "")
        SN = ont["SN"].replace(" ", "")
        IDX = ont["IDX"] + 1
        print("| {:^3} | {:^6} | {:^16} |".format(IDX, FSP, SN))


def existingLookup(comm, command, olt):
    lookupType = input("Buscar cliente por serial, por nombre o por Datos de OLT [S | N | D] : ")
    if lookupType == "S":
        SN = input("Ingrese el Serial del Cliente a buscar : ")
        (FRAME,SLOT,PORT,ID,NAME,STATE) = serialSearch(comm,command,SN)
        (VLAN,PLAN,IPADDRESS,SPID) = wan(comm, command, SLOT, PORT, ID)
        (temp, pwr) = verifyValues(comm, command, SLOT, PORT, ID)
        print(
            f"""
FRAME               :   {FRAME}
SLOT                :   {SLOT}
PORT                :   {PORT}
ID                  :   {ID}
NAME                :   {NAME}
STATE               :   {STATE}
VLAN                :   {VLAN}
PLAN                :   {PLAN}
IP                  :   {IPADDRESS}
SPID                :   {SPID}
TEMPERATURA         :   {temp}
POTENCIA            :   {pwr}
"""
        )
    elif lookupType == "D":
        FRAME = input("Ingrese frame de cliente : ")
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        command(f"display ont info {FRAME} {SLOT} {PORT} {ID} | no-more")
        sleep(3)
        (value, regex) = parser(comm, existingCond, "m")
        (_, sDESC) = check(value, existing["DESC"]).span()
        (_, sCF) = check(value, existing["CF"]).span()
        (eCF, _) = check(value, existing["RE"]).span()
        (eDESC, _) = check(value, existing["LDC"]).span()
        NAME = value[sDESC:eDESC].replace("\n", "")
        STATE = value[sCF:eCF].replace("\n", "")
        VLAN = wan(comm, command, SLOT, PORT, ID)
        (VLAN,PLAN,IPADDRESS,SPID) = wan(comm, command, SLOT, PORT, ID)
        (temp, pwr) = verifyValues(comm, command, SLOT, PORT, ID)
        print(
            f"""
FRAME               :   {FRAME}
SLOT                :   {SLOT}
PORT                :   {PORT}
ID                  :   {ID}
NAME                :   {NAME}
STATE               :   {STATE}
VLAN                :   {VLAN}
PLAN                :   {PLAN}
IP                  :   {IPADDRESS}
SPID                :   {SPID}
TEMPERATURA         :   {temp}
POTENCIA            :   {pwr}
""")

    elif lookupType == "N":
        NAME = input("Ingrese el Nombre del Cliente a buscar : ")
        command(f'display ont info by-desc "{NAME}" | no-more')
        sleep(3)
        (value, regex) = parser(comm, existingCond, "m")
        (_, s) = regex[0]
        (e, _) = regex[len(regex) - 1]
        print(value[s:e])
    
    else:
        print(f'la opcion "{lookupType}" no existe')
