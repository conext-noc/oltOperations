from helpers.spidInfo import getSPID
from helpers.onuIdInfo import addONU, addOnuService
from helpers.ontCheck import verifyValues
from helpers.templateGen import template

providerMap = {
    "INTER": 1101,
    "VNET": 1102
}


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
    if ("N" in type):
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        NAME = input("Ingrese nombre del cliente : ")
        PROVIDER = input("Ingrese proevedor de cliente [INTER | VNET] : ")
        SN = input("Ingrese serial de cliente : ")
        PLAN = input("Ingrese plan de cliente : ")
        LP = input("Ingrese Line-Profile [prueba | INET] : ")
        SRV = input("Ingrese Service-Profile [PRUEBA_BRIDGE | FTTH] : ")
        SPID = getSPID(comm, command, enter)
        print(SPID)
        ID = addONU(comm, command, enter, SLOT, PORT, SN,
                    providerMap[PROVIDER], NAME, SRV, LP)
    elif ("P" in type):
        SLOT = input("Ingrese slot de cliente : ")
        PORT = input("Ingrese puerto de cliente : ")
        ID = input("Ingrese el id del cliente : ")
        NAME = input("Ingrese nombre del cliente : ")
        SPID = input("Ingrese el Service Port ID del cliente : ")
        PROVIDER = input("Ingrese proevedor de cliente [INTER | VNET] : ")
        SN = input("Ingrese serial de cliente : ")
        PLAN = input("Ingrese plan de cliente : ")
    if (ID != ""):
        (temp, pwr) = verifyValues(comm, command, enter, SLOT, PORT, ID)
        proceed = input(
            f"La potencia del ONT es : {pwr} y la temperatura es : {temp} \nquieres proceder con la instalacion? [y|n] : ")
        if (proceed == "y"):
            addOnuService(command, enter, SPID,
                          providerMap[PROVIDER], SLOT, PORT, ID, PLAN)
            print(template(SLOT, PORT, ID, NAME, olt,
                           PROVIDER, PLAN, temp, pwr, SPID))
            return
        if (proceed == "n"):
            reason = input("Por que no se le asignara servicio? : ")
            print(template(SLOT, PORT, ID, NAME, olt,
                           PROVIDER, PLAN, temp, pwr, SPID, reason))
            return
