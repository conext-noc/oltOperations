from helpers.spidHandler import availableSpid, verifySPID
from helpers.addHandler import addONU, addOnuService
from helpers.opticalCheck import opticalValues
from helpers.formatter import colorFormatter

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}


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
        LP = input("Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS | Bridging] : ").upper()
        SRV = input("Ingrese Service-Profile [Prueba | FTTH | Bridging] : ").upper()
        SPID = availableSpid(comm, command)
        (ID, PROVIDER, fail) = addONU(comm, command, FRAME, SLOT, PORT, SN, NAME, SRV, LP)
        if fail != None:
            resp = colorFormatter(fail, "fail")
            print(resp)
            return
    elif action == "IP":
        FRAME = input("Ingrese frame de cliente : ").upper()
        SLOT = input("Ingrese slot de cliente : ").upper()
        PORT = input("Ingrese puerto de cliente : ").upper()
        ID = input("Ingrese el id del cliente : ").upper()
        NAME = input("Ingrese nombre del cliente : ").upper()
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
