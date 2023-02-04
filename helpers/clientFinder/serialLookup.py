from helpers.utils.decoder import check, checkIter, decoder
from helpers.failHandler.fail import failChecker
from time import sleep
from re import sub
from helpers.clientFinder.ontType import typeCheck

existingCond = "-----------------------------------------------------------------------------"
existing = {
    "FSP": "F/S/P                   : ",
    "LP": "Line profile name    : ",
    "SRV": "Service profile name : ",
    "ONTID": "ONT-ID                  : ",
    "CF": "Control flag            : ",
    "CS": "Config state",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
    "LDT": "Last down time          : ",
    "LUT": "Last up time            : ",
    "LDGT": "Last dying gasp time    : ",
}

# improve this to return an object

def serialSearch(comm, command, SN):
    FAIL = None
    command(f"display ont info by-sn {SN} | no-more")
    sleep(3)
    val = decoder(comm)
    regex = checkIter(val,existingCond)
    FAIL = failChecker(val)
    if FAIL == None:
        (_, s) = regex[0]
        (e, _) = regex[len(regex) - 1]
        value = val[s:e]
        (_, eFSP) = check(value, existing["FSP"]).span()
        valFSP = value[eFSP : eFSP + 6].replace("\n", "")
        reFSP = checkIter(valFSP, "/")
        (_, eSLOT) = reFSP[0]
        (_, ePORT) = reFSP[1]
        SLOT = valFSP[eSLOT : eSLOT + 1].replace("\n", "")
        PORT = valFSP[ePORT : ePORT + 2].replace("\n", "")
        (_, eID) = check(value, existing["ONTID"]).span()
        (_, sDESC) = check(value, existing["DESC"]).span()
        (eDESC, sLDC) = check(value, existing["LDC"]).span()
        (eLDC,sLDT) = check(value, existing["LUT"]).span()
        (_, sCF) = check(value, existing["CF"]).span()
        (eCF, sRE) = check(value, existing["RE"]).span()
        (eRE, _) = check(value, existing["CS"]).span()
        FRAME = 0
        ID = value[eID : eID + 3].replace("\n", "")
        NAME = sub(" +", " ", value[sDESC:eDESC]).replace("\n", "")
        STATE = value[sCF:eCF].replace("\n", "")
        STATUS = value[sRE:eRE]
        LDC = value[sLDC:eLDC]
        data = {"frame":FRAME, "slot":SLOT, "port":PORT,"onu_id":ID}
        ONT_TYPE = typeCheck(comm,command,data)
        return (FRAME, SLOT, PORT, ID, NAME,STATUS, STATE,ONT_TYPE,LDC, FAIL)
    else:
        return (None, None, None, None, None, None,None,None,None, FAIL)
