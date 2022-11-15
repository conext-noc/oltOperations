from helpers.failHandler import failChecker
from helpers.formatter import colorFormatter
from helpers.outputDecoder import parser, check
from helpers.clientDataLookup import lookup
from time import sleep
from helpers.spidHandler import availableSpid
from helpers.addHandler import addOnuService


condition = "-----------------------------------------------------------------------------"
newCond = "----------------------------------------------------------------------------"
newCondFSP = "F/S/P               : "
newCondSn = "Ont SN              : "


def newLookup(comm, command, olt):
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
        aSN = result[eSN : eSN + 16].replace("\n", "").replace(" ", "")
        aFSP = result[eFSP : eFSP + 6].replace("\n", "").replace(" ", "")
        client.append({"FSP": aFSP, "SN": aSN, "IDX": ont})
    print("| {:^3} | {:^6} | {:^16} |".format("IDX", "F/S/P", "SN"))
    for ont in client:
        FSP = ont["FSP"].replace(" ", "")
        SN = ont["SN"].replace(" ", "")
        IDX = ont["IDX"] + 1
        print("| {:^3} | {:^6} | {:^16} |".format(IDX, FSP, SN))


def existingLookup(comm, command, olt):
    FAIL = None
    lookupType = input("Buscar cliente por serial, por nombre o por Datos de OLT [S | N | D] : ").upper()
    data = lookup(comm, command, olt, lookupType)
    FAIL = data["fail"]
    if FAIL == None:
        if lookupType == "S" or lookupType == "D":
            str1 = f"""
    FRAME               :   {data["frame"]}
    SLOT                :   {data["slot"]}
    PORT                :   {data["port"]}
    ID                  :   {data["id"]}
    NAME                :   {data["name"]}
    STATE               :   {data["state"]}
    STATUS              :   {data["status"]}
    LAST DOWN CAUSE     :   {data["ldc"]}
    ONT TYPE            :   {data["type"]}
    SN                  :   {data["sn"]}
    IP                  :   {data["ipAdd"]}
    TEMPERATURA         :   {data["temp"]}
    POTENCIA            :   {data["pwr"]}
                """
            str2 = ""
            if(len(data["wan"]) > 0):
                for idx, wanData in enumerate(data["wan"]):
                    str2 += f"""
    VLAN_{idx}              :   {wanData["VLAN"]}
    PLAN_{idx}              :   {wanData["PLAN"]}
    SPID_{idx}              :   {wanData["SPID"]}
                    """
            res = str1 + str2
            res = colorFormatter(res, "ok")
            print(res)
            if(len(data["wan"]) <= 0):
                addSpid = input("desea agregar SPID? [Y | N] : ").upper()
                if(addSpid == "Y"):
                    spid = availableSpid(comm, command)
                    print(colorFormatter(f"El SPID que se le agregara al cliente es : {spid}", "ok"))
                    PROVIDER = input("Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ").upper()
                    PLAN = input("Ingrese plan de cliente : ").upper()
                    addOnuService(command, comm, spid, PROVIDER, data["frame"], data["slot"], data["port"], data["id"], PLAN)
        elif lookupType == "N":
            command(f'display ont info by-desc "{data["name"]}" | no-more')
            sleep(3)
            (value, regex) = parser(comm, condition, "m")
            FAIL = failChecker(value)
            if FAIL == None:
                (_, s) = regex[0]
                (e, _) = regex[len(regex) - 1]
                print(value[s:e])
    else:
        FAIL = colorFormatter(FAIL, "fail")
        print(FAIL)
