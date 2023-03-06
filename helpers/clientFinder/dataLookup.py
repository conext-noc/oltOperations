from time import sleep
from helpers.clientFinder.ontType import typeCheck
from helpers.failHandler.fail import failChecker
from helpers.utils.decoder import check, decoder

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
    "SN": "SN                      : ",
}


def dataLookup(comm, command, data):
    command(f"display ont info {data['frame']} {data['slot']} {data['port']} {data['onu_id']} | no-more")
    sleep(3)
    value = decoder(comm)
    data["fail"] = failChecker(value)
    if data["fail"] == None:
        (_, sDESC) = check(value, existing["DESC"]).span()
        (_, sCF) = check(value, existing["CF"]).span()
        (eCF, sRE) = check(value, existing["RE"]).span()
        (_,sLDT) = check(value, existing["LDT"]).span()
        (eLDT,_) = check(value, existing["LDGT"]).span()
        (eDESC, sLDC) = check(value, existing["LDC"]).span()
        (eLDC, _) = check(value, existing["LUT"]).span()
        (eRE, _) = check(value, existing["CS"]).span()
        (_, sSN) = check(value, existing["SN"]).span()
        
        data["run_state"] = value[sRE:eRE].replace("\n", "").replace("\r", "")
        data["name"] = value[sDESC:eDESC].replace("\n", "").replace("\r", "")
        data["control_flag"] = value[sCF:eCF].replace("\n", "").replace("\r", "")
        data["sn"] = value[sSN : sSN + 16].replace("\n", "").replace("\r", "")
        data["last_down_cause"]=value[sLDC:eLDC].replace("\n", "").replace("\r", "")
        data["last_down_date"]=value[sLDT:eLDT][:10].replace("\n", "").replace("\r", "")
        data["last_down_time"]=value[sLDT:eLDT][11:].replace("\n", "").replace("\r", "")
        data["device"] = typeCheck(comm, command, data)
    return data
