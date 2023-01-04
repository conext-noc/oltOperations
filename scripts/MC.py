from time import sleep
from helpers.clientFinder.dataLookup import dataLookup
from helpers.operations.addHandler import addOnuService
from helpers.operations.newAddHandler import addOnuServiceNew
from helpers.operations.spid import availableSpid, spidCalc, verifySPID
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.plans import plans
from helpers.utils.sheets import modify


def modifyClient(comm, command, quit, olt, act):
    proceed = None
    action = inp(
        """
Que cambio se realizara? 
  > (CT)    :   Cambiar Titular
  > (CO)    :   Cambiar ONT
  > (CP)    :   Cambiar Plan & Vlan
  > (ES)    :   Eliminar Service Port
  > (AS)    :   Agregar Service Port
  > (AV)    :   Agregar Voip [Solo OLT 1 (X15 nueva)]
$ """
    )
    lookupType = inp(
        "Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
    data = dataLookup(comm, command, olt, lookupType)
    proceed = display(data, "A")
    if not proceed:
        log(colorFormatter("Cancelando...", "warning"))
        quit()
        return
    if action == "CT":
        NEW_NAME = inp("Ingrese el Nuevo Titular del cliente : ")
        command(f"interface gpon {data['frame']}/{data['slot']}")
        command(f'ont modify {data["port"]} {data["id"]} desc "{NEW_NAME}" ')
        command("quit")
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha cambiado el nombre a '{NEW_NAME}'",
                "success",
            )
        )
        modify(data["sn"], NEW_NAME, "NAME")
        quit()
        return
    if action == "CO":
        NEW_SN = inp("Ingrese el Nuevo serial de ONT del cliente : ")
        command(f"interface gpon {data['frame']}/{data['slot']}")
        command(f'ont modify {data["port"]} {data["id"]} sn "{NEW_SN}" ')
        command("quit")
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha cambiado el serial a '{NEW_SN}'",
                "success",
            )
        )
        modify(data["sn"], NEW_SN, "SN")
        quit()
        return
    if action == "CP":
        if olt != "1":
            for wan in data["wan"]:
                command(f"undo service-port {wan['spid']}")
            addOnuService(comm,command,data)
        else:
            data['planName'] = inp("Ingrese el Nuevo plana instalar : ")
            data['wan'] = plans[data['planName']]
            for wanData in data["wan"]:
                command(f"undo service-port {wanData['spid']}")
            addOnuServiceNew(comm,command,data)
            verifySPID(comm, command, data)
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha Cambiado el plan y vlan a {data['planName']} @ {data['wan']['vlan']}",
                "info",
            )
        )
        modify(data["sn"], data['planName'], "PLAN")
        modify(data["sn"], data['wan']['vlan'], "PROVIDER")
        quit()
        return
    if action == "ES":
        log("| {:^3} | {:^4} | {:^6} |".format("IDX", "VLAN", "SPID"))
        for idx, wan in enumerate(data["wan"]):
            log("| {:^3} | {:^4} | {:^6} |".format(
                idx, wan["vlan"], wan["spid"]))
        DEL_SPID = int(inp("Ingrese el SPID a eliminar : "))
        command(f"undo service-port {DEL_SPID}")
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha eliminado el SPID {DEL_SPID}",
                "info",
            )
        )
        quit()
        return
    if action == "AS":
        if olt != "1":
            data["wan"][0]["spid"] = availableSpid(comm, command)
            addOnuService(comm, command, data)
            verifySPID(comm, command, data)
            log(
                colorFormatter(
                    f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha Agregado el plan y vlan a {data['plan']} @ {data['vlan']}",
                    "info",
                )
            )
            quit()
            return
        NEW_PLAN = inp("Ingrese el Nuevo Plan del cliente : ")
        data["wan"][0]["vlan"] = plans[NEW_PLAN]["vlan"]
        data["wan"][0]["plan"] = plans[NEW_PLAN]["plan"]
        data["gemPort"] = plans[NEW_PLAN]["gemPort"]
        addOnuServiceNew(comm, command, data)
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha Agregado el plan y vlan a {NEW_PLAN} @ {data['wan'][0]['vlan']}",
                "info",
            )
        )
        quit()
        return
        
    if action == "AV":
        data["wan"][0]["spid"] = spidCalc(data)["V"]
        log(colorFormatter(
            f"SPID PARA AGG {data['spid']}, FUNCION AUN NO DISPONIBLE"), "info")
        quit()
        return
