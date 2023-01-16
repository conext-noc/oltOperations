from time import sleep
from helpers.clientFinder.ontType import typeCheck
from helpers.clientFinder.optical import opticalValues
from helpers.clientFinder.serialLookup import serialSearch
from helpers.clientFinder.wan import wan
from helpers.failHandler.fail import failChecker
from helpers.utils.decoder import check, decoder
from helpers.utils.printer import inp
from re import sub

existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
    "CS": "Config state            :",
    "SN": "SN                      : ",
    "LUT": "Last up time            : ",
}


def dataLookup(comm, command, olt, lookup_type, all=True):
    """
    This module retrieves the clients data from the cli
    
    comm        : connection client
    command     : fnc to send command with enter
    olt         : which olt belongs the client
    lookup_type : type of search, by sn, by name, by olt data
    
    all ==> display all the data available | false = for installation data concern
    """
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

    if lookup_type == "S":
        SN = inp("Ingrese el Serial del Cliente a buscar : ")
        (
            FRAME,
            SLOT,
            PORT,
            ID,
            NAME,
            STATUS,
            STATE,
            ONT_TYPE,
            LDC,
            FAIL,
        ) = serialSearch(comm, command, SN)

    if lookup_type == "D":
        FRAME = inp("Ingrese frame de cliente  : ")
        SLOT = inp("Ingrese slot de cliente   : ")
        PORT = inp("Ingrese puerto de cliente : ")
        ID = inp("Ingrese el onu id del cliente : ")
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
            (eRE, _) = check(value, existing["CS"]).span()
            (_, sSN) = check(value, existing["SN"]).span()
            STATUS = value[sRE:eRE].replace("\n", "").replace("\r", "")
            NAME = value[sDESC:eDESC].replace("\n", "").replace("\r", "")
            STATE = value[sCF:eCF].replace("\n", "").replace("\r", "")
            LDC = value[sLDC:eLDC].replace("\n", "").replace("\r", "")
            SN = value[sSN : sSN + 16].replace("\n", "").replace("\r", "")
            data = {"frame":FRAME, "slot":SLOT, "port":PORT,"onu_id":ID}
            ONT_TYPE = typeCheck(comm, command, data)
        else:
            FAIL = fail

    if FAIL == None:
        (IPADDRESS, WAN) = wan(comm, command, FRAME, SLOT, PORT, ID, olt)
        data = {"frame":FRAME, "slot":SLOT, "port":PORT,"onu_id":ID}
        (TEMP, PWR) = opticalValues(comm, command, data, False)
        return {
            "fail": FAIL,
            "name": sub(" +", " ", NAME).replace("\n", "").replace("\r", ""),
            "olt": olt,
            "frame": FRAME,
            "slot": SLOT,
            "port": PORT,
            "onu_id": ID,
            "sn": SN,
            "last_down_cause": LDC,
            "state": STATE,
            "status": STATUS,
            "device": ONT_TYPE,
            "ip_address": IPADDRESS,
            "wan": WAN,
            "temp": TEMP,
            "pwr": PWR,
        }
    if FAIL != None:
        return {"fail": FAIL}
