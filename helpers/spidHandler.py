from helpers.outputDecoder import decoder, check, checkIter
from helpers.failHandler import failChecker
from helpers.formatter import colorFormatter
from helpers.fileHandler import dictConverter
from re import sub
from helpers.printer import log

conditionSpidOnt = "CTRL_C to break"
condition = "-----------------------------------------------------------------------------"
spidHeader = "SPID,ID,ATT,PORT_TYPE,F/S,/P,VPI,VCI,FLOW_TYPE,FLOW_PARA,RX,TX,STATE,"
conditionSPID = """Next valid free service virtual port ID: """
spidCheck = {
    "index": "Index               : ",
    "id": "VLAN ID             : ",
    "attr": "VLAN attr           : ",
    "endAttr": "Port type",
    "plan": "Outbound table name : ",
    "adminStatus": "Admin status        : ",
    "status": "State               : ",
    "endStatus": "Label               :",
}

planX2Maps = {
    "7": "OZ_FAMILY",
    "8": "FTTH_INTERNET_10Mbps",
    "9": "FTTH_INTERNET_15",
    "15": "FTTH_INTERNET_30Mbps",
    "16": "FTTH_INTERNET_5Mbps",
    "18": "FTTH_UNLIMITED",
    "19": "FTTH_VOIP",
    "30": "FTTH_INTERNET_MAX",
    "32": "OZ_MAGICAL",
    "33": "OZ_NEXT",
    "34": "OZ_LIFT",
    "36": "OZ_UP",
    "44": "OZ_EMPRENDE",
    "45": "OZ_INICIATE",
    "46": "OZ_CONECTA",
    "47": "OZ_SKY",
    "48": "OZ_MAX",
    "49": "OZ_PLUS",
    "50": "DEDICADO 10 Mbps",
}

planX15Maps = {
    "6": "OZ_LIFT",
    "7": "OZ_FAMILY",
    "9": "FTTH_VOIP",
    "15": "UNLIMITED",
    "16": "FTTH_INTERNET_10Mbps",
    "20": "FTTH_INTERNET_5Mbps",
    "23": "FTTH_INTERNET_15",
    "25": "FTTH_INTERNET_30Mbps",
    "39": "OZ_MAGICAL",
    "40": "OZ_NEXT",
    "41": "OZ EMPRENDE",
    "42": "OZ_EMPRENDE",
    "43": "OZ_INICIATE",
    "44": "OZ_CONECTA",
    "45": "OZ_SKY",
    "46": "OZ_MAX",
    "47": "OZ_PLUS",
    "48": "DEDICADO 10 Mbps",
    "49": "OZ_UP",
}


def ontSpid(comm, command, FRAME, SLOT, PORT, ID):
    command(f" display  service-port  port  {FRAME}/{SLOT}/{PORT}  ont  {ID}  |  no-more")
    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        limits = checkIter(value, condition)
        (_, s) = limits[1]
        (e, _) = limits[2]
        data = spidHeader + sub(" +", " ", value[s : e - 2]).replace(" ", ",")
        data = dictConverter(data)
        return (data, None)
    else:
        return (None, fail)


def availableSpid(comm, command):
    command("display service-port next-free-index")
    command("")
    value = decoder(comm)
    (_, e) = check(value, conditionSPID).span()
    spid = value[e : e + 5].replace(" ", "").replace("\n", "")
    return spid


def verifySPID(comm, command, spid):
    command(f"display service-port {spid} | no-more")
    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        (_, sIdx) = check(value, spidCheck["index"]).span()
        (eIdx, sId) = check(value, spidCheck["id"]).span()
        (eId, sAtt) = check(value, spidCheck["attr"]).span()
        (eAtt, _) = check(value, spidCheck["endAttr"]).span()
        (_, sPlan) = check(value, spidCheck["plan"]).span()
        (ePlan, sAS) = check(value, spidCheck["adminStatus"]).span()
        (eAS, sState) = check(value, spidCheck["status"]).span()
        (eState, _) = check(value, spidCheck["endStatus"]).span()
        INDEX = value[sIdx:eIdx].replace(" ", "").replace("\n", "")
        VLAN = value[sId:eId].replace(" ", "").replace("\n", "")
        ATTR = value[sAtt:eAtt].replace(" ", "").replace("\n", "")
        PLAN = value[sPlan:ePlan].replace(" ", "").replace("\n", "")
        ADMIN_STATE = value[sAS:eAS].replace(" ", "").replace("\n", "")
        STATE = value[sState:eState].replace(" ", "").replace("\n", "")
        val = """
INDEX           :   {}
VLAN            :   {}
ATTR            :   {}
PLAN            :   {}
ADMIN STATE     :   {}
STATE           :   {}
        """.format(
            INDEX, VLAN, ATTR, PLAN, ADMIN_STATE, STATE
        )
        msg = colorFormatter(val, "ok")
        log(msg)
    else:
        fail = colorFormatter(value, "fail")
        log(fail)
        spid = availableSpid(comm, command)
        msg = colorFormatter(f"No se agrego el SPID, el siguiente SPID libre es {spid}", "warning")
        log(msg)
