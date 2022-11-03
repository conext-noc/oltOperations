from helpers.spidHandler import availableSpid, verifySPID
from helpers.addHandler import addONU, addOnuService
from helpers.opticalCheck import opticalValues
from helpers.formatter import colorFormatter
from helpers.serialLookup import serialSearch
from time import sleep
from re import sub
from helpers.outputDecoder import check, decoder
from helpers.failHandler import failChecker

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}

existing = {
    "CF": "Control flag            : ",
    "RE": "Run state               : ",
    "DESC": "Description             : ",
    "LDC": "Last down cause         : ",
}


def confirm(comm, command, olt, action):
    FRAME = None
    SLOT = None
    PORT = None
    NAME = None
    PROVIDER = None
    SN = None
    PLAN = None
    LP = None
    SRV = None
    SPID = None
    ID = None
    if action == "IN":
        FRAME = input("Ingrese frame de cliente : ").upper()
        SLOT = input("Ingrese slot de cliente : ").upper()
        PORT = input("Ingrese puerto de cliente : ").upper()
        NAME = input("Ingrese nombre del cliente : ").upper()
        SN = input("Ingrese serial de cliente : ").upper()
        PLAN = input("Ingrese plan de cliente : ").upper()
        LP = input("Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS | Bridging] : ")
        SRV = input("Ingrese Service-Profile [Prueba | FTTH | Bridging] : ")
        SPID = availableSpid(comm, command)
        (ID, PROVIDER, fail) = addONU(comm, command, FRAME, SLOT, PORT, SN, NAME, SRV, LP)
        if fail != None:
            resp = colorFormatter(fail, "fail")
            print(resp)
            return
    elif action == "IP":
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
                (eDESC, _) = check(value, existing["LDC"]).span()
                NAME = value[sDESC:eDESC].replace("\n", "")
                NAME = sub(" +", " ", NAME).replace("\n", "")
            else:
                fail = colorFormatter(fail, "fail")
                print(fail)
        res = f"""
        FRAME               :   {FRAME}
        SLOT                :   {SLOT}
        PORT                :   {PORT}
        ID                  :   {ID}
        NAME                :   {NAME}
        """
        res = colorFormatter(res, "ok")
        print(res)
        PROVIDER = input("Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ").upper()
        PLAN = input("Ingrese plan de cliente : ").upper()
        SPID = availableSpid(comm, command)
        addVlan = input("Se agregara vlan al puerto? (es bridge) [Y | N] : ").upper()
        if addVlan == "Y":
            command(f"interface gpon {FRAME}/{SLOT}")
            command(f" ont  port  native-vlan  {PORT} {ID}  eth  1  vlan  {providerMap[PROVIDER]} ")
            command("quit")
    if ID != None and ID != "F":
        resp = colorFormatter(f"El SPID que se le agregara al cliente es : {SPID}", "ok")
        print(resp)
        (temp, pwr) = opticalValues(comm, command, FRAME, SLOT, PORT, ID, True)
        proceed = input(
            f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [Y | N] : "
        ).upper()
        if proceed == "Y":
            addOnuService(command, SPID, providerMap[PROVIDER], FRAME, SLOT, PORT, ID, PLAN)
            verifySPID(comm, command, SPID)
            PLAN = PLAN[3:]
            template = """
    {} {}/{}/{}/{} 
    OLT {} {} {}
    TEMPERATURA :   {}
    POTENCIA    :   {}
    SPID        :   {}""".format(
                NAME, FRAME, SLOT, PORT, ID, olt, PROVIDER, PLAN, temp, pwr, SPID
            )
            res = colorFormatter(template, "success")
            print(res)
            return
        if proceed == "N":
            reason = input("Por que no se le asignara servicio? : ").upper()
            PLAN = PLAN[3:]
            template = """
    {} {}/{}/{}/{} 
    OLT {} {} {}
    TEMPERATURA :   {}
    POTENCIA    :   {}
    SPID        :   {}
    RAZÓN       :   {}""".format(
                NAME, FRAME, SLOT, PORT, ID, olt, PROVIDER, PLAN, temp, pwr, SPID, reason
            )
            res = colorFormatter(template, "success")
            print(res)
            return
