from helpers.formatter import colorFormatter
from helpers.outputDecoder import decoder, check
from helpers.failHandler import failChecker
from helpers.serialLookup import serialSearch

ip = "IPv4 address               : "
endIp = "Subnet mask"
vlan = "Manage VLAN                : "


def verifyReset(comm, command):
    lookupType = input("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ").upper()
    if(lookupType == "D"):
        FRAME = input("Ingrese frame de cliente : ").upper()
        SLOT = input("Ingrese slot de cliente : ").upper()
        PORT = input("Ingrese puerto de cliente : ").upper()
        ID = input("Ingrese el id del cliente : ").upper()
        # AUTO BUSCAR NOMBRE DE CLIENTE
    elif(lookupType == "S"):
        SN = input("Ingrese serial de cliente : ").upper()
        (FRAME,SLOT,PORT,ID,NAME,STATE, FAIL) = serialSearch(comm,command,SN)

    command(f'display ont wan-info  {FRAME}/{SLOT}  {PORT} {ID}  ')

    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        (_,s) = check(value,ip).span()
        (e,_) = check(value,endIp).span()

        IP = value[s : e].replace("\n", "").replace(" ", "")
        print(f"El cliente tiene la IP : {IP}")
    else:
        fail = colorFormatter(fail, "warning")
        print(fail)
