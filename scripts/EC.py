from helpers.formatter import colorFormatter
from helpers.serialLookup import serialSearch
from helpers.getWanData import wan
from time import sleep
from helpers.outputDecoder import check, decoder
from helpers.failHandler import failChecker
from re import sub

existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
}


def delete(comm, command, OLT):
    FRAME = None
    SLOT = None
    PORT = None
    ID = None
    NAME = None
    STATE = None
    lookupType = input("Buscar cliente por serial, por nombre o por Datos de OLT [S | D] : ").upper()
    if lookupType == "S":
        SN = input("Ingrese el Serial del Cliente a buscar : ").upper()
        (FRAME, SLOT, PORT, ID, NAME, STATE, fail) = serialSearch(comm, command, SN)
    elif lookupType == "D":
        FRAME = input("Ingrese frame de cliente : ").upper()
        SLOT = input("Ingrese slot de cliente : ").upper()
        PORT = input("Ingrese puerto de cliente : ").upper()
        ID = input("Ingrese el id del cliente : ").upper()
        command(f"display ont info {FRAME} {SLOT} {PORT} {ID} | no-more")
        sleep(3)
        value = decoder(comm)
        fail = failChecker(value)
        if fail == None:
            (_, sDESC) = check(value, existing["DESC"]).span()
            (_, sCF) = check(value, existing["CF"]).span()
            (eCF, _) = check(value, existing["RE"]).span()
            (eDESC, _) = check(value, existing["LDC"]).span()
            NAME = value[sDESC:eDESC].replace("\n", "")
            STATE = value[sCF:eCF].replace("\n", "")
        else:
            fail = colorFormatter(fail, "fail")
            print(fail)
    NAME = sub(" +", " ", NAME).replace("\n", "")
    resp = colorFormatter(
        f"""
    FRAME               :   {FRAME}
    SLOT                :   {SLOT}
    PORT                :   {PORT}
    ID                  :   {ID}
    NAME                :   {NAME}
    STATE               :   {STATE}
    """,
        "ok",
    )
    print(resp)
    proceed = input("Desea continuar? [Y | N]   :   ").upper()
    if proceed == "Y":
        (_, WAN, FAIL) = wan(comm, command, FRAME, SLOT, PORT, ID, OLT)
        if FAIL == None:
            for wanData in WAN:
                spid = wanData["SPID"]
                command(f" undo  service-port  {spid}")
            command(f"interface gpon {FRAME}/{SLOT}")
            command(f"ont delete {PORT} {ID}")
            command("quit")
            resp = colorFormatter(f"{NAME} {FRAME}/{SLOT}/{PORT}/{ID} de OLT {OLT} ha sido eliminado", "ok")
            print(resp)
        else:
            fail = colorFormatter(FAIL, "fail")
            print(fail)
