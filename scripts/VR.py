from helpers.formatter import colorFormatter
from helpers.outputDecoder import decoder, check
from helpers.failHandler import failChecker
from helpers.serialLookup import serialSearch
from time import sleep
from helpers.printer import inp, log

ip = "IPv4 address               : "
endIp = "Subnet mask"
vlan = "Manage VLAN                : "


def verifyReset(comm, command,quit):
    FRAME = ""
    SLOT = ""
    PORT = ""
    ID = ""
    NAME = ""
    FAIL = None
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ").upper()
    if lookupType == "D":
        FRAME = inp("Ingrese frame de cliente : ").upper()
        SLOT = inp("Ingrese slot de cliente : ").upper()
        PORT = inp("Ingrese puerto de cliente : ").upper()
        ID = inp("Ingrese el id del cliente : ").upper()
        command(f"display ont info {FRAME} {SLOT} {PORT} {ID} | no-more")
        sleep(3)
        value = decoder(comm)
        fail = failChecker(value)
        if fail == None:
            (_, sDESC) = check(value, "Description             : ").span()
            (eDESC, _) = check(value, "Last down cause         : ").span()
            NAME = value[sDESC:eDESC].replace("\n", "")
            log(
                f"""
    NOMBRE              :   {NAME}
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}"""
            )
    elif lookupType == "S":
        SN = inp("Ingrese serial de cliente : ").upper()
        (FRAME, SLOT, PORT, ID, NAME, STATE, FAIL) = serialSearch(comm, command, SN)

    command(f"display ont wan-info  {FRAME}/{SLOT}  {PORT} {ID}  ")

    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        if FAIL == None:
            (_, s) = check(value, ip).span()
            (e, _) = check(value, endIp).span()
            IP = value[s:e].replace("\n", "").replace(" ", "")
            msg = colorFormatter(f"El cliente tiene la IP : {IP}", "ok")
            log(msg)
            quit(5)
            return
        else:
            msg = colorFormatter(FAIL, "warning")
            log(msg)
            quit(5)
            return
    else:
        fail = colorFormatter(fail, "warning")
        log(fail)
        quit(5)
        return
