from time import sleep
from helpers.utils.decoder import decoder, check, checkIter
from helpers.failHandler.fail import failChecker
from helpers.utils.printer import log, colorFormatter
from helpers.fileFormatters.fileHandler import dataToDict

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


def ontSpid(comm, command, client):
    command(
        f"display service-port port {client['frame']}/{client['slot']}/{client['port']} ont {client['onu_id']}  |  no-more")
    sleep(2)
    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        limits = checkIter(value, condition)
        (_, s) = limits[1]
        (e, _) = limits[2]
        data = dataToDict(spidHeader, value[s: e - 2])
        return (data, None)
    else:
        return (None, fail)


def availableSpid(comm, command):
    command("display service-port next-free-index")
    command("")
    value = decoder(comm)
    (_, e) = check(value, conditionSPID).span()
    spid = value[e: e + 5].replace(" ", "").replace("\n", "")
    return spid


def verifySPID(comm, command, data):
    command(f"""display service-port {data['wan'][0]['spid']}
""")
    command("")
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
        log(colorFormatter(val, "ok"))
    else:
        log(colorFormatter(value, "fail"))
        spid = availableSpid(comm, command)
        log(colorFormatter(
            f"No se agrego el SPID, el siguiente SPID libre es {spid}", "warning"))


def spidCalc(data):
    SPID = 12288*(int(data["slot"]) - 1) + 771 * \
        int(data["port"]) + 3 * int(data["onu_id"])
    return {
        "I": SPID,
        "P": SPID + 1,
        "V": SPID + 2
    }
