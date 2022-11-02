from helpers.outputDecoder import check, decoder
from helpers.failHandler import failChecker
from helpers.formatter import colorFormatter

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


def getFreeSpid(comm, command):
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
        print(msg)
    else:
        fail = colorFormatter(value, "fail")
        print(fail)
        spid = getFreeSpid(comm, command)
        msg = colorFormatter(f"No se agrego el SPID, el siguiente SPID libre es {spid}", "warning")
        print(msg)
