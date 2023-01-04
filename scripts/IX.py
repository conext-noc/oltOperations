from helpers.clientFinder.dataLookup import dataLookup
from helpers.clientFinder.newLookup import newLookup
from helpers.clientFinder.ontType import typeCheck
from helpers.clientFinder.optical import opticalValues
from helpers.clientFinder.wanInterface import preWan
from helpers.operations.addHandler import addONU, addOnuService
from helpers.operations.spid import availableSpid, verifySPID
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.utils.sheets import insert
from helpers.utils.template import approved, denied

def confirm(comm, command, quit, olt, action):
    {
    "fail": None,
    "name": None,
    "olt": olt,
    "frame": None,
    "slot": None,
    "port": None,
    "id": None,
    "sn": None,
    "ldc": None,
    "state": None,
    "status": None,
    "type": None,
    "ipAdd": None,
    "planName": None,
    "wan": [{"spid": None, "vlan": None, "plan": None, "provider": None, }],
    "temp": None,
    "pwr": None,
    "lineProfile": None,
    "srvProfile": None,
    "device": None,
}
    if "N" in action:
        (client["sn"], FSP) = newLookup(comm, command, olt)
        val = inp("desea continuar? [Y|N] : ").upper()
        proceed = True if val == "Y" and client["sn"] != None else False
        if proceed:
            client["frame"] = int(FSP.split("/")[0])
            client["slot"] = int(FSP.split("/")[1])
            client["port"] = int(FSP.split("/")[2])
            client["name"] = inp("Ingrese nombre del cliente : ")[:56]
            client["nif"] = inp("Ingrese el NIF del cliente [V123 | J123]: ")
            client["lineProfile"] = inp(
                "Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS ] : "
            )
            client["srvProfile"] = inp("Ingrese Service-Profile [ FTTH ] : ")
            client["wan"][0]["spid"] = availableSpid(comm, command)

            (client["id"], client["fail"]) = addONU(comm, command, client)
        else:
            log(colorFormatter("SN no aparece en OLT, Saliendo...", "warning"))
            quit()
            return

    elif "P" in action:
        lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
        client = dataLookup(comm, command, olt, lookupType)
        if client["fail"] == None:
            proceed = display(client, "I")
            client["nif"] = (
                inp("Ingrese el NIF del cliente [V123 | J123]: ") if proceed else None
            )
            client["lineProfile"] = (
                inp("Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS ] : ")
                if proceed
                else None
            )
            client["srvProfile"] = (
                inp("Ingrese Service-Profile [ FTTH ] : ") if proceed else None
            )
            print(client)
            client["wan"][0]["spid"] = availableSpid(comm, command) if proceed else None
        else:
            log(colorFormatter(client["fail"], "fail"))
            quit()
            return

    if client["id"] != None and proceed:
        log(
            colorFormatter(
                f'El SPID que se le agregara al cliente es : {client["wan"][0]["spid"]}', "ok"
            )
        )
        (client["temp"], client["pwr"]) = opticalValues(comm, command, client, True)

        value = inp(
            f"""
  La potencia del ONT es : {client["pwr"]} y la temperatura es : {client["temp"]}
  quieres proceder con la instalacion? [Y | N] : """
        )
        install = True if value == "Y" else False if value == "N" else None
        
        if not install:
                    reason = inp("Por que no se le asignara servicio? : ").upper()
                    denied(client, reason)
                    quit()
                    return
        client["device"] = typeCheck(comm, command, client)
        log(colorFormatter(f"El tipo de ONT del cliente es {client['device']}", "ok"))
        
        addOnuService(comm, command, client)
        
        verifySPID(comm, command, client)
        wksArr = approved(client)
        insert(wksArr)
        quit()
        return

    else:
        log(colorFormatter("Cancelando...", "warning"))
        quit()
        return
