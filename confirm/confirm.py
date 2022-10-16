from helpers.spidInfo import getSPID, verifySPID
from helpers.onuIdInfo import addONU, addOnuService
from helpers.ontCheck import verifyValues
from helpers.templateGen import template

providerMap = {"INTER": 1101, "VNET": 1102, "PUBLICAS": 1104}


def confirm(comm, enter, command, olt, type):
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
    if "N" in type:
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        NAME = input("Ingrese nombre del cliente : ")
        PROVIDER = input("Ingrese proevedor de cliente [INTER | VNET | PUBLICAS] : ")
        SN = input("Ingrese serial de cliente : ")
        PLAN = input("Ingrese plan de cliente : ")
        LP = input(
            "Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS | Bridging] : "
        )
        SRV = input("Ingrese Service-Profile [Prueba | FTTH | Bridging] : ")
        SPID = getSPID(comm, command, enter)
        print(f"El SPID que se le agregara al cliente es : {SPID}")
        ID = addONU(
            comm, command, enter, SLOT, PORT, SN, providerMap[PROVIDER], NAME, SRV, LP
        )
    elif "P" in type:
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        NAME = input("Ingrese nombre del cliente : ")
        PROVIDER = input("Ingrese proevedor de cliente [INTER | VNET] : ")
        SN = input("Ingrese serial de cliente : ")
        PLAN = input("Ingrese plan de cliente : ")
        SPID = getSPID(comm, command, enter)
    if ID != "" and ID != "F":
        print(f"El SPID que se le agregara al cliente es : {SPID}")
        (temp, pwr) = verifyValues(comm, command, enter, SLOT, PORT, ID)
        proceed = input(
            f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [Y | N] : "
        )
        if proceed == "Y":
            addOnuService(
                command, enter, SPID, providerMap[PROVIDER], SLOT, PORT, ID, PLAN
            )
            verifySPID(comm, command, enter, SPID)
            print(template(SLOT, PORT, ID, NAME, olt, PROVIDER, PLAN, temp, pwr, SPID))
            return
        if proceed == "N":
            reason = input("Por que no se le asignara servicio? : ")
            print(
                template(
                    SLOT, PORT, ID, NAME, olt, PROVIDER, PLAN, temp, pwr, SPID, reason
                )
            )
            return
