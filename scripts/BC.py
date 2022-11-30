from helpers.failHandler import failChecker
from helpers.printer import inp, log, colorFormatter
from helpers.outputDecoder import parser, check
from helpers.clientDataLookup import lookup
from time import sleep
from helpers.spidHandler import availableSpid
from helpers.addHandler import addOnuService


condition = "-----------------------------------------------------------------------------"
providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

def existingLookup(comm, command, olt,quit):
    FAIL = None
    lookupType = inp("Buscar cliente por serial, por nombre o por Datos de OLT [S | N | D] : ").upper()
    if lookupType == "D":
        lookup(comm, command, olt, lookupType)
        return
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
    TEMPERATURA         :   {data["temp"]}
    POTENCIA            :   {data["pwr"]}
    IP                  :   {data["ipAdd"]}
                """
            str2 = ""
            if(len(data["wan"]) > 0):
                for idx, wanData in enumerate(data["wan"]):
                    str2 += f"""
    VLAN_{idx}              :   {wanData["VLAN"]}
    PLAN_{idx}              :   {wanData["PLAN"]}
    SPID_{idx}              :   {wanData["SPID"]}
    STATE_{idx}             :   {wanData["STATE"]}
                    """
            res = colorFormatter(str1, "ok") + colorFormatter(str2, "ok")
            log(res)
            if(len(data["wan"]) <= 0):
                addSpid = inp("desea agregar SPID? [Y | N] : ").upper()
                if(addSpid == "Y"):
                    NAME = data["name"]
                    FRAME = data["frame"]
                    SLOT = data["slot"]
                    PORT = data["port"]
                    ID = data["id"]
                    spid = availableSpid(comm, command)
                    log(colorFormatter(f"El SPID que se le agregara al cliente es : {spid}", "ok"))
                    PROVIDER = inp("Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ").upper()
                    PLAN = inp("Ingrese plan de cliente : ").upper()
                    addOnuService(command, comm, spid, providerMap[PROVIDER], FRAME, SLOT, PORT, ID, PLAN)
                    res = colorFormatter(f"Cliente : {NAME} @ {FRAME}/{SLOT}/{PORT}/{ID} en OLT {olt} se le ha agregado en el SPID {spid} con proveedor {PROVIDER} y con plan {PLAN}", "ok")
                    log(res)
                    quit()
            quit()
        elif lookupType == "N":
            command(f'display ont info by-desc "{data["name"]}" | no-more')
            sleep(3)
            (value, regex) = parser(comm, condition, "m")
            FAIL = failChecker(value)
            if FAIL == None:
                (_, s) = regex[0]
                (e, _) = regex[len(regex) - 1]
                log(value[s:e])
                quit()
            else:
                FAIL = colorFormatter(FAIL, "fail")
                log(FAIL)
                quit()
                return
    else:
        FAIL = colorFormatter(FAIL, "fail")
        log(FAIL)
        quit()
        return
