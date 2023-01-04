from time import sleep
from helpers.clientFinder.dataLookup import dataLookup
# from helpers.operations.addHandler import addOnuService
from helpers.operations.addHandler import addOnuServiceNew
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
    client = dataLookup(comm, command, olt, lookupType)
    proceed = display(client, "A")
    if not proceed:
        log(colorFormatter("Cancelando...", "warning"))
        quit()
        return
    if action == "CT":
        NEW_NAME = inp("Ingrese el Nuevo Titular del cliente : ")
        command(f"interface gpon {client['frame']}/{client['slot']}")
        command(f'ont modify {client["port"]} {client["id"]} desc "{NEW_NAME}" ')
        command("quit")
        log(
            colorFormatter(
                f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['id']} @ OLT {client['olt']} se le ha cambiado el nombre a '{NEW_NAME}'",
                "success",
            )
        )
        modify(client["sn"], NEW_NAME, "NAME")
        quit()
        return
    if action == "CO":
        NEW_SN = inp("Ingrese el Nuevo serial de ONT del cliente : ")
        command(f"interface gpon {client['frame']}/{client['slot']}")
        command(f'ont modify {client["port"]} {client["id"]} sn "{NEW_SN}" ')
        command("quit")
        log(
            colorFormatter(
                f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['id']} @ OLT {client['olt']} se le ha cambiado el serial a '{NEW_SN}'",
                "success",
            )
        )
        modify(client["sn"], NEW_SN, "SN")
        quit()
        return
    if action == "CP":
        client['planName'] = inp("Ingrese el Nuevo plana instalar : ")
        client['wan'] = plans[client['planName']]
        for wanData in client["wan"]:
            command(f"undo service-port {wanData['spid']}")
        addOnuServiceNew(comm,command,client)
        verifySPID(comm, command, client)
        log(
            colorFormatter(
                f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['id']} @ OLT {client['olt']} se le ha Cambiado el plan y vlan a {client['planName']} @ {client['wan']['vlan']}",
                "info",
            )
        )
        modify(client["sn"], client['planName'], "PLAN")
        modify(client["sn"], client['wan']['vlan'], "PROVIDER")
        quit()
        return
    if action == "ES":
        log("| {:^3} | {:^4} | {:^6} |".format("IDX", "VLAN", "SPID"))
        for idx, wan in enumerate(client["wan"]):
            log("| {:^3} | {:^4} | {:^6} |".format(
                idx, wan["vlan"], wan["spid"]))
        DEL_SPID = int(inp("Ingrese el SPID a eliminar : "))
        command(f"undo service-port {DEL_SPID}")
        log(
            colorFormatter(
                f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['id']} @ OLT {client['olt']} se le ha eliminado el SPID {DEL_SPID}",
                "info",
            )
        )
        quit()
        return
    if action == "AS":
        NEW_PLAN = inp("Ingrese el Nuevo Plan del cliente : ")
        client["wan"][0]["vlan"] = plans[NEW_PLAN]["vlan"]
        client["wan"][0]["plan"] = plans[NEW_PLAN]["plan"]
        client["gemPort"] = plans[NEW_PLAN]["gemPort"]
        addOnuServiceNew(comm, command, client)
        verifySPID(comm, command, client)
        log(
            colorFormatter(
                f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['id']} @ OLT {client['olt']} se le ha Agregado el plan y vlan a {NEW_PLAN} @ {client['wan'][0]['vlan']}",
                "info",
            )
        )
        quit()
        return
        
    if action == "AV":
        client["wan"][0]["spid"] = spidCalc(client)["V"]
        log(colorFormatter(
            f"SPID PARA AGG {client['spid']}, FUNCION AUN NO DISPONIBLE"), "info")
        quit()
        return
