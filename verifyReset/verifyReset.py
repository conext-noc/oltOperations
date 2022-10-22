from helpers.outputDecoder import parser, check
from helpers.failHandler import failChecker
from helpers.serialLookup import serialSearch

ip = "IPv4 address               : "
vlan = "Manage VLAN                : "


def verifyReset(comm, command, enter):
    lookupType = input("Buscar cliente por serial o por datos [S | D] : ")
    if(lookupType == "D"):
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        NAME = input("Ingrese nombre del cliente : ")

        command(f"interface gpon 0/{SLOT}")
        enter()
        command(f'display ont wan-info {PORT} {ID} | include "IPv4 address" ')
        enter()

        (value, re) = parser(comm, ip, "s")
        if re != None:
            endIp = re.span()[1]
            IP = value[endIp : endIp + 15].replace("\n", "").replace(" ", "")
            print(f"El cliente {NAME} tiene la IP : {IP}")
        else:
            print(f"El cliente {NAME} tiene reset")
    elif(lookupType == "S"):
        SN = input("Ingrese serial de cliente : ")
        (FRAME,SLOT,PORT,ID,NAME,STATE) = serialSearch(comm,command,enter,SN)
        command(f"interface gpon {FRAME}/{SLOT}")
        enter()
        command(f'display ont wan-info {PORT} {ID} | include "IPv4 address" ')
        enter()

        (value, re) = parser(comm, ip, "s")
        if re != None:
            endIp = re.span()[1]
            IP = value[endIp : endIp + 15].replace("\n", "").replace(" ", "")
            print(f"El cliente {NAME} tiene la IP : {IP}")
        else:
            print(f"El cliente {NAME} tiene reset")


def verifyWAN(comm, command, enter, SLOT, PORT, ID):
    command(f"interface gpon 0/{SLOT}")
    enter()
    command(f"display ont wan-info {PORT} {ID}")
    enter()
    (value, re) = parser(comm, vlan, "s")
    fail = failChecker(value)
    if fail == None:
        (_, e) = re.span()
        vUsed = value[e : e + 4]
        print(f"Al ONT se le ha agregado la vlan {vUsed}")
        return vUsed
    else:
        print(fail)
        return fail
