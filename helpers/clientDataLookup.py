from datetime import datetime
from re import sub
from time import sleep
from helpers.fileHandler import dataToDict
from helpers.outputDecoder import check, decoder, parser
from helpers.failHandler import failChecker
from helpers.serialLookup import serialSearch
from helpers.getWanData import wan
from helpers.opticalCheck import opticalValues
from helpers.printer import colorFormatter
from helpers.ontTypeHandler import typeCheck
from helpers.printer import inp, log

existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
    "CS": "Config state            :",
    "SN": "SN                      : ",
    "LUT": "Last up time            : ",
}
infoHeader = "NA,F/,S/P,ID,SN,controlFlag,runState,configState,matchState,protectSide,NA"
descHeader = "NA,F/,S/P,ID,NAME1,NAME2,NAME3,NAME4,NAME5,NAME6,NAME7,NA"

condition = "-----------------------------------------------------------------------------"
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "
newCondTime = "Ont autofind time   : "

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}


def lookup(comm, command, OLT, lookupType, all=True):
    """
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
    clients = []
    if lookupType == "S":
        SN = inp("Ingrese el Serial del Cliente a buscar : ").upper()
        (FRAME, SLOT, PORT, ID, NAME, STATUS, STATE, ONT_TYPE,
         LDC, FAIL) = serialSearch(comm, command, SN)
    elif lookupType == "D":
        FRAME = inp("Ingrese frame de cliente  : ").upper()
        SLOT = inp("Ingrese slot de cliente   : ").upper()
        PORT = inp("Ingrese puerto de cliente : ").upper()
        ID = inp("Ingrese el id del cliente : ").upper()
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
            STATUS = value[sRE:eRE].replace("\n", "")
            NAME = value[sDESC:eDESC].replace("\n", "")
            STATE = value[sCF:eCF].replace("\n", "")
            LDC = value[sLDC:eLDC]
            SN = value[sSN:sSN+16]
            ONT_TYPE = typeCheck(comm, command, FRAME, SLOT, PORT, ID)
        else:
            FAIL = fail
    elif lookupType == "N":
        NAME = inp("Ingrese el Nombre del Cliente a buscar : ")
        command(f'display ont info by-desc "{NAME}" | no-more ')
        sleep(5)
        (value, regex) = parser(comm, condition, "m")
        FAIL = failChecker(value)
        portRange= []
        if FAIL == None:
            ttlPorts = len(regex) // 6
            for port in range(0,ttlPorts):
                portRange.append({"sInfo":regex[port+1][1], "eInfo": regex[port + 2][0], "sDesc": regex[port + 3][1], "eDesc":regex[port + 4][0]})
            for info in portRange:
                valueInfo = dataToDict(infoHeader,value[info["sInfo"]:info["eInfo"]])
                valueDesc = dataToDict(descHeader,value[info["sDesc"]:info["eDesc"]])
                for (info,desc) in zip(valueInfo,valueDesc):
                    if info["ID"] == desc["ID"]:
                        name = ""
                        SLOT = int(desc["S/P"].split("/")[0])
                        PORT = int(desc["S/P"].split("/")[1])
                        for i in range(1, 7):
                            NAME = str(desc[f"NAME{i}"]) if str(
                                desc[f"NAME{i}"]) != "nan" else ""
                            name += NAME + " "
                        clients.append({
                            "frame":0,
                            "slot":SLOT,
                            "port":PORT,
                            "id":desc["ID"],
                            "name":name,
                            "controlFlag":info["controlFlag"],
                            "runState":info["runState"],
                            "sn": info["SN"]
                        })
    else:
        log(colorFormatter(f"Opcion {lookupType} no existe", "fail"))
        return {
            "fail": f"Opcion {lookupType} no existe",
        }
    
    
    if FAIL == None and lookupType != "N":
        if all:
            log(colorFormatter("getting wan data", "info"))
            (IPADDRESS, WAN) = wan(comm, command, FRAME, SLOT, PORT, ID, OLT)
            log(colorFormatter("getting optical data", "info"))
            (TEMP, PWR) = opticalValues(
                comm, command, FRAME, SLOT, PORT, ID, False)
        return {
            "fail": FAIL,
            "name": sub(" +", " ", NAME).replace("\n", ""),
            "frame": FRAME,
            "slot": SLOT,
            "port": PORT,
            "id": ID,
            "sn": SN,
            "ldc": LDC,
            "state": STATE.replace("\n", ""),
            "status": STATUS.replace("\n", ""),
            "type": ONT_TYPE,
            "ipAdd": IPADDRESS,
            "wan": WAN,
            "temp": TEMP,
            "pwr": PWR,
        }
    elif FAIL == None and lookupType == "N":
        return {"data":clients,"fail":None}
    elif FAIL != None and lookupType != "N":
        return {
            "fail": FAIL,
            "name": NAME,
            "frame": FRAME,
            "slot": SLOT,
            "port": PORT,
            "id": ID,
            "sn": SN,
            "ldc": LDC,
            "state": STATE,
            "status": STATUS,
            "type": ONT_TYPE,
            "ipAdd": IPADDRESS,
            "wan": WAN,
            "temp": TEMP,
            "pwr": PWR,
        }
    elif FAIL != None and lookupType == "N":
        return {
            "fail": FAIL
        }
    else:
        log(colorFormatter(f"FATAL, OCURRIO UN ERROR", "fail"))
        return {
            "fail": f"FATAL, OCURRIO UN ERROR",
        }

def newLookup(comm, command, olt):
    SN_NEW = inp("Ingrese el Serial del Cliente a buscar : ").upper()
    SN_FINAL = None
    FSP_FINAL = None
    client = []
    command("  display  ont  autofind  all  |  no-more  ")
    sleep(5)
    (value, regex) = parser(comm, newCond, "m")
    for ont in range(len(regex) - 1):
        (_, s) = regex[ont]
        (e, _) = regex[ont + 1]
        result = value[s:e]
        (_, eFSP) = check(result, newCondFSP).span()
        (_, eSN) = check(result, newCondSn).span()
        (_, eT) = check(result, newCondTime).span()
        aSN = result[eSN: eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[eFSP: eFSP + 6].replace("\n", "").replace(" ", "")
        aT = result[eT: eT + 19].replace("\n", "")
        t1 = datetime.strptime(aT, "%Y-%m-%d %H:%M:%S")
        t2 = datetime.fromisoformat(str(datetime.now()))
        clientTime = t2 - t1
        client.append({"FSP": aFSP, "SN": aSN, "IDX": ont,
                      "TIME": clientTime.days})
    log("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "SN"))
    for ont in client:
        count = []
        FSP = ont["FSP"].replace(" ", "")
        SN = ont["SN"].replace(" ", "")
        IDX = ont["IDX"] + 1
        TIME = ont["TIME"]
        if SN_NEW == SN and TIME <= 10:
            SN_FINAL = SN
            FSP_FINAL = FSP
            log(colorFormatter(
                "| {:^3} | {:^6} | {:^16} |".format(IDX, FSP, SN), "success"))
            count.append({"SN": SN_FINAL, "FSP": FSP_FINAL})
        elif SN_NEW == SN and TIME > 10:
            log(colorFormatter("| {:^3} | {:^6} | {:^16} |".format(
                IDX, FSP, SN), "warning"))
        else:
            log("| {:^3} | {:^6} | {:^16} |".format(IDX, FSP, SN))
        if (len(count) > 1):
            log("| {:^3} | {:^6} | {:^16} |".format(
                "IDX", "F/S/P", "SN"
            ))
            for idx, res in enumerate(count):
                log("| {:^3} | {:^6} | {:^16} |".format(idx,res["FSP"],res["SN"]))
            ix = inp("SELECCIONE EL INDEX DEL SERIAL A UTILIZAR : ")
            SN_FINAL = res[ix]["SN"]
            FSP_FINAL = res[ix]["FSP"]
    return (SN_FINAL, FSP_FINAL)
