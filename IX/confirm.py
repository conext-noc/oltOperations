from helpers.spidInfo import getFreeSpid, verifySPID
from helpers.addHandler import addONU, addOnuService
from helpers.ontCheck import verifyValues
from helpers.templateGen import template

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}


def confirm(comm, command, olt, action):
    SLOT = ""
    PORT = ""
    NAME = ""
    PROVIDER = ""
    SN = ""
    PLAN = ""
    LP = ""
    SRV = ""
    SPID = ""
    ID = ""
    if action == "IN":
        FRAME = input("Ingrese frame de cliente : ")
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        NAME = input("Ingrese nombre del cliente : ")
        SN = input("Ingrese serial de cliente : ")
        PLAN = input("Ingrese plan de cliente : ")
        LP = input(
            "Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS | Bridging] : "
        )
        SRV = input("Ingrese Service-Profile [Prueba | FTTH | Bridging] : ")
        SPID = getFreeSpid(comm, command)
        print(f"El SPID que se le agregara al cliente es : {SPID}")
        (ID, PROVIDER) = addONU(
            comm, command, FRAME,SLOT, PORT, SN, NAME, SRV, LP
        )
    elif action == "IP":
        FRAME = input("Ingrese frame de cliente : ")
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        NAME = input("Ingrese nombre del cliente : ")
        PROVIDER = input("Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ")
        PLAN = input("Ingrese plan de cliente : ")
        SPID = getFreeSpid(comm, command)
    if ID != "" and ID != "F":
        print(f"El SPID que se le agregara al cliente es : {SPID}")
        (temp, pwr) = verifyValues(comm, command,FRAME, SLOT, PORT, ID)
        proceed = input(
            f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [Y | N] : "
        )
        if proceed == "Y":
            addOnuService(
                command, SPID, providerMap[PROVIDER], FRAME,SLOT, PORT, ID, PLAN
            )
            verifySPID(comm, command, SPID)
            print(template(FRAME,SLOT, PORT, ID, NAME, olt, PROVIDER, PLAN, temp, pwr, SPID))
            return
        if proceed == "N":
            reason = input("Por que no se le asignara servicio? : ")
            print(
                template(
                   FRAME,SLOT, PORT, ID, NAME, olt, PROVIDER, PLAN, temp, pwr, SPID, reason
                )
            )
            return
