from helpers.failHandler import failChecker
from helpers.printer import inp, log, colorFormatter
from helpers.outputDecoder import parser
from helpers.clientDataLookup import lookup
from time import sleep
from helpers.spidHandler import availableSpid
from helpers.addHandler import addOnuService
from helpers.displayClient import display


condition = "-----------------------------------------------------------------------------"
providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}


def existingLookup(comm, command, olt, quit):
    FAIL = None
    lookupType = inp(
        "Buscar cliente por serial, por nombre o por Datos de OLT [S | N | D] : ").upper()
    data = lookup(comm, command, olt, lookupType)
    FAIL = data["fail"]
    if FAIL == None:
        if lookupType != "N":
            display(data, "B")
            if (len(data["wan"]) <= 0):
                addSpid = inp("desea agregar SPID? [Y | N] : ").upper()
                if (addSpid == "Y"):
                    NAME = data["name"]
                    FRAME = data["frame"]
                    SLOT = data["slot"]
                    PORT = data["port"]
                    ID = data["id"]
                    spid = availableSpid(comm, command)
                    log(colorFormatter(
                        f"El SPID que se le agregara al cliente es : {spid}", "ok"))
                    PROVIDER = inp(
                        "Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ").upper()
                    PLAN = inp("Ingrese plan de cliente : ").upper()
                    addOnuService(
                        command, comm, spid, providerMap[PROVIDER], FRAME, SLOT, PORT, ID, PLAN)
                    res = colorFormatter(
                        f"Cliente : {NAME} @ {FRAME}/{SLOT}/{PORT}/{ID} en OLT {olt} se le ha agregado en el SPID {spid} con proveedor {PROVIDER} y con plan {PLAN}", "ok")
                    log(res)
                    quit()
            quit()
        else:
            clients = data["data"]
            log("| {:^6} | {:^3} | {:^40} | {:^10} | {:^15} | {:^16} |".format(
                "F/S/P", "ID", "NAME", "STATUS", "STATE", "SN"
            )
            )
            for client in clients:
                FRAME = client["frame"]
                SLOT = client["slot"]
                PORT = client["port"]
                FSP = f"{FRAME}/{SLOT}/{PORT}"
                resp = "| {:^6} | {:^3} | {:^40} | {:^10} | {:^15} | {:^16} |".format(
                    FSP, client["id"], client["name"], client["runState"], client["controlFlag"], client["sn"])
                log(resp)
            quit()
            return
    else:
        FAIL = colorFormatter(FAIL, "fail")
        log(FAIL)
        quit()
        return
