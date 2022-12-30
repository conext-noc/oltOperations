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
    data = {
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
        "wan": [{"spid":None, "vlan": None, "plan": None,"provider": None,}],
        "temp": None,
        "pwr": None,
        "lineProfile": None,
        "srvProfile": None,
        "device": None,
    }
    if "N" in action:
        (data["sn"], FSP) = newLookup(comm, command, olt)
        val = inp("desea continuar? [Y|N] : ").upper()
        proceed = True if val == "Y" and data["sn"] != None else False
        if proceed:
            data["frame"] = int(FSP.split("/")[0])
            data["slot"] = int(FSP.split("/")[1])
            data["port"] = int(FSP.split("/")[2])
            data["name"] = inp("Ingrese nombre del cliente : ")[:56]
            data["nif"] = inp("Ingrese el NIF del cliente [V123 | J123]: ")
            data["lineProfile"] = inp(
                "Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS ] : "
            )
            data["srvProfile"] = inp("Ingrese Service-Profile [ FTTH ] : ")
            data["wan"][0]["spid"] = availableSpid(comm, command)

            (data["id"], data["fail"]) = addONU(comm, command, data)
        else:
            log(colorFormatter("SN no aparece en OLT, Saliendo...", "warning"))
            quit()
            return

    elif "P" in action:
        lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
        data = dataLookup(comm, command, olt, lookupType)
        if data["fail"] == None:
            proceed = display(data, "I")
            data["nif"] = (
                inp("Ingrese el NIF del cliente [V123 | J123]: ") if proceed else None
            )
            data["lineProfile"] = (
                inp("Ingrese Line-Profile [PRUEBA_BRIDGE | INET | IP PUBLICAS ] : ")
                if proceed
                else None
            )
            data["srvProfile"] = (
                inp("Ingrese Service-Profile [ FTTH ] : ") if proceed else None
            )
            print(data)
            data["wan"][0]["spid"] = availableSpid(comm, command) if proceed else None
        else:
            log(colorFormatter(data["fail"], "fail"))
            quit()
            return

    if data["id"] != None and proceed:
        log(
            colorFormatter(
                f'El SPID que se le agregara al cliente es : {data["wan"][0]["spid"]}', "ok"
            )
        )
        (data["temp"], data["pwr"]) = opticalValues(comm, command, data, True)

        value = inp(
            f"""
  La potencia del ONT es : {data["pwr"]} y la temperatura es : {data["temp"]}
  quieres proceder con la instalacion? [Y | N] : """
        )
        install = True if value == "Y" else False if value == "N" else None
        
        if not install:
                    reason = inp("Por que no se le asignara servicio? : ").upper()
                    denied(data, reason)
                    quit()
                    return
        data["device"] = typeCheck(comm, command, data)
        log(colorFormatter(f"El tipo de ONT del cliente es {data['device']}", "ok"))
        
        addOnuService(comm, command, data)
        
        verifySPID(comm, command, data)
        wksArr = approved(data)
        insert(wksArr)
        quit()
        return

    else:
        log(colorFormatter("Cancelando...", "warning"))
        quit()
        return
