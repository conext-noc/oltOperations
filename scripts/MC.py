from helpers.clientFinder.lookup import lookup
from helpers.operations.addHandler import addOnuServiceNew
from helpers.operations.spid import spidCalc, verifySPID
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.plans import PLANS
from helpers.utils.sheets import modify


def modifyClient(comm, command, quit, olt, act):
    """
    comm        :   ssh connection handler [class]
    command     :   sends ssh commands [func]
    quit        :   terminates the ssh connection [func]
    olt         :   defines the selected olt [var:str]
    action      :   defines the type of lookup/action of the client [var:str]
    
    This module modifies the data of a given client
    """
    proceed = None
    action = inp(
        """
Que cambio se realizara? 
  > (CT)    :   Cambiar Titular
  > (CO)    :   Cambiar ONT
  > (CP)    :   Cambiar Plan & Vlan
  > (CV)    :   Cambiar Proveedor
  > (ES)    :   Eliminar Service Port
  > (AS)    :   Agregar Service Port
  > (AV)    :   Agregar Voip [Solo OLT 1 (X15 nueva)]
$ """
    )
    lookupType = inp(
        "Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
    client = lookup(comm, command, olt, lookupType)
    if client["fail"] == None:
        proceed = display(client, "A")
        if not proceed:
            log(colorFormatter("Cancelando...", "warning"))
            quit()
            return
        if action == "CT":
            NEW_NAME = inp("Ingrese el Nuevo Titular del cliente : ")
            command(f"interface gpon {client['frame']}/{client['slot']}")
            command(f'ont modify {client["port"]} {client["onu_id"]} desc "{NEW_NAME}" ')
            command("quit")
            log(
                colorFormatter(
                    f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} @ OLT {client['olt']} se le ha cambiado el nombre a '{NEW_NAME}'",
                    "success",
                )
            )
            modify(client["sn"], NEW_NAME, "NAME")
            quit()
            return
        if action == "CO":
            NEW_SN = inp("Ingrese el Nuevo serial de ONT del cliente : ")
            command(f"interface gpon {client['frame']}/{client['slot']}")
            command(f'ont modify {client["port"]} {client["onu_id"]} sn "{NEW_SN}" ')
            command("quit")
            log(
                colorFormatter(
                    f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} @ OLT {client['olt']} se le ha cambiado el serial a '{NEW_SN}'",
                    "success",
                )
            )
            modify(client["sn"], NEW_SN, "SN")
            quit()
            return
        if action == "CP":
            for wanData in client["wan"]:
                command(f"undo service-port {wanData['spid']}")
            client['plan_name'] = inp("Ingrese el Nuevo plan a instalar : ")
            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]
            command(f"interface gpon {client['frame']}/{client['slot']}")
            command(f"ont modify {client['port']} {client['onu_id']} ont-lineprofile-id {client['wan'][0]['line_profile']}")
            command(f"ont modify {client['port']} {client['onu_id']} ont-srvprofile-id {client['wan'][0]['srv_profile']}")
            command("quit")
            addOnuServiceNew(comm, command, client)
            verifySPID(comm, command, client)
            log(
                colorFormatter(
                    f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} @ OLT {client['olt']} se le ha Cambiado el plan y vlan a {client['plan_name']} @ {client['wan'][0]['vlan']}",
                    "success",
                )
            )
            modify(client["sn"], client['plan_name'], "PLAN")
            modify(client["sn"], client['wan'][0]['vlan'], "PROVIDER")
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
                    f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} @ OLT {client['olt']} se le ha eliminado el SPID {DEL_SPID}",
                    "info",
                )
            )
            quit()
            return
        if action == "AS":
            client['plan_name'] = inp("Ingrese el Nuevo plana instalar : ")
            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]
            addOnuServiceNew(comm, command, client)
            verifySPID(comm, command, client)
            log(
                colorFormatter(
                    f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} @ OLT {client['olt']} se le ha Agregado el plan y vlan a {client['plan_name']} @ {client['wan'][0]['vlan']}",
                    "info",
                )
            )
            quit()
            return
        if action == "CV":
            for wanData in client["wan"]:
                command(f"undo service-port {wanData['spid']}")
            client['plan_name'] = inp("Ingrese el Nuevo plan a instalar : ")
            client["wan"][0] = PLANS[client["olt"]][client["plan_name"]]
            addOnuServiceNew(comm, command, client)
            verifySPID(comm, command, client)
            log(
                colorFormatter(
                    f"Al cliente {client['name']} {client['frame']}/{client['slot']}/{client['port']}/{client['onu_id']} @ OLT {client['olt']} se le ha Agregado el plan y vlan a {client['plan_name']} @ {client['wan'][0]['vlan']}",
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
    else:
        log(colorFormatter(f"{client['fail']}","fail"))