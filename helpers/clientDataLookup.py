from re import sub
from time import sleep
from helpers.outputDecoder import check, decoder
from helpers.failHandler import failChecker
from helpers.serialLookup import serialSearch
from helpers.getWanData import wan
from helpers.opticalCheck import opticalValues
from helpers.formatter import colorFormatter
from helpers.ontTypeHandler import typeCheck

existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
    "CS": "Config state            :",
    "SN":"SN                      : ",
    "LUT": "Last up time            : ",
}


def lookup(comm, command, OLT, lookupType, previous=True):
    FAIL = None
    NAME = None
    FRAME = None
    SLOT = None
    PORT = None
    ID = None
    LDC = None
    STATE = None
    STATUS = None
    IPADDRESS = None
    WAN = []
    TEMP = None
    PWR = None
    ONT_TYPE = None
    SN = None
    if lookupType == "S":
        SN = input("Ingrese el Serial del Cliente a buscar : ").upper()
        (FRAME, SLOT, PORT, ID, NAME,STATUS, STATE,ONT_TYPE,LDC, FAIL) = serialSearch(comm, command, SN)
    elif lookupType == "D":
        FRAME = input("Ingrese frame de cliente  : ").upper()
        SLOT = input("Ingrese slot de cliente   : ").upper()
        PORT = input("Ingrese puerto de cliente : ").upper()
        ID = input("Ingrese el id del cliente : ").upper()
        command(f"display ont info {FRAME} {SLOT} {PORT} {ID} | no-more")
        sleep(3)
        value = decoder(comm)
        fail = failChecker(value)
        if fail == None:
            (_, sDESC) = check(value, existing["DESC"]).span()
            (_, sCF) = check(value, existing["CF"]).span()
            (eCF, sRE) = check(value, existing["RE"]).span()
            (eDESC, sLDC) = check(value, existing["LDC"]).span()
            (eLDC, _) = check(value, existing["LUT"]).span()
            (eRE,_) = check(value,existing["CS"]).span()
            (_,sSN) = check(value, existing["SN"]).span()
            STATUS = value[sRE:eRE].replace("\n", "")
            NAME = value[sDESC:eDESC].replace("\n", "")
            STATE = value[sCF:eCF].replace("\n", "")
            LDC = value[sLDC:eLDC]
            SN = value[sSN:sSN+16]
            ONT_TYPE = typeCheck(comm,command,FRAME,SLOT,PORT,ID)
        else:
            FAIL = fail
    elif lookupType == "N":
        NAME = input("Ingrese el Nombre del Cliente a buscar : ")
    else:
        print(colorFormatter(f"Opcion {lookupType} no existe", "fail"))
        return {
            "fail": f"Opcion {lookupType} no existe",
        }
    if FAIL == None:
        if previous:
            print(colorFormatter("getting wan data", "info"))
            (IPADDRESS, WAN, FAIL) = wan(comm, command, FRAME, SLOT, PORT, ID, OLT)
            print(colorFormatter("getting optical data", "info"))
            (TEMP, PWR) = opticalValues(comm, command, FRAME, SLOT, PORT, ID, False)
        return {
            "fail": FAIL,
            "name": sub(" +", " ", NAME).replace("\n", ""),
            "frame": FRAME,
            "slot": SLOT,
            "port": PORT,
            "id": ID,
            "sn":SN,
            "ldc": LDC,
            "state": STATE.replace("\n", ""),
            "status": STATUS.replace("\n", ""),
            "type": ONT_TYPE,
            "ipAdd": IPADDRESS,
            "wan": WAN,
            "temp": TEMP,
            "pwr": PWR,
        }
    else:
        return {
            "fail": FAIL,
            "name": NAME,
            "frame": FRAME,
            "slot": SLOT,
            "port": PORT,
            "id": ID,
            "sn":SN,
            "ldc": LDC,
            "state": STATE,
            "status":STATUS,
            "type": ONT_TYPE,
            "ipAdd": IPADDRESS,
            "wan": WAN,
            "temp": TEMP,
            "pwr": PWR,
        }
