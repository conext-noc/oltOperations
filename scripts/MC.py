from helpers.clientFinder.dataLookup import dataLookup
from helpers.operations.addHandler import addOnuService
from helpers.operations.spid import availableSpid, spidCalc, verifySPID
from helpers.utils.decoder import decoder
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.plans import oldPlans


def modifyClient(comm, command, quit, olt):
    proceed = None
    action = inp(
        """
Que cambio se realizara? 
  > (CT)    :   Cambiar Titular
  > (CO)    :   Cambiar ONT
  > (CP)    :   Cambiar Plan & Vlan
  > (ES)    :   Eliminar Service Port
  > (AS)    :   Agregar Service Port
$ """
    )
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
    data = dataLookup(comm, command, olt, lookupType)
    proceed = display(data, "A")
    if not proceed:
        log(colorFormatter("Cancelando...", "warning"))
        return
    if action == "CT":
        NEW_NAME = inp("Ingrese el Nuevo Titular del cliente")
        command(f"interface gpon {data['frame']}/{data['slot']}")
        command(f'ont modify {data["port"]} {data["id"]} desc "{NEW_NAME}" ')
        command("quit")
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha cambiado el nombre a '{NEW_NAME}'",
                "success",
            )
        )
        return
    if action == "CO":
        NEW_SN = inp("Ingrese el Nuevo serial de ONT del cliente")
        command(f"interface gpon {data['frame']}/{data['slot']}")
        command(f'ont modify {data["port"]} {data["id"]} sn "{NEW_SN}" ')
        command("quit")
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha cambiado el serial a '{NEW_SN}'",
                "success",
            )
        )
        """"""
        return
    if action == "CP" and olt != "1":
        log("| {:^3} | {:^4} | {:^6} |".format("IDX", "VLAN", "SPID"))
        for idx, wan in enumerate(data["wan"]):
            log("| {:^3} | {:^4} | {:^6} |".format(idx, wan["vlan"], wan["spid"]))
        IDX = int(inp("Ingrese el INDEX del service-port a cambiar : "))
        NEW_PLAN = inp("Ingrese el Nuevo Plan del cliente : ")
        NEW_VLAN = inp("Ingrese la Nueva Vlan del cliente : ")
        command(f"undo service-port {data['wan'][IDX]['spid']}")
        PLAN_ID = oldPlans[data['olt']][NEW_PLAN]
        command(
            f" service-port {data['wan'][IDX]['spid']} vlan {NEW_VLAN} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['id']} gemport 14 multi-service user-vlan {NEW_VLAN} tag-transform transparent inbound traffic-table index {PLAN_ID} outbound traffic-table index {PLAN_ID}"
        )
        verifySPID(comm,command,data)
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha Cambiado el plan y vlan a {NEW_PLAN} @ {NEW_VLAN}",
                "info",
            )
        )
        return
    if action == "ES":
        log("| {:^3} | {:^4} | {:^6} |".format("IDX", "VLAN", "SPID"))
        for idx, wan in enumerate(data["wan"]):
            log("| {:^3} | {:^4} | {:^6} |".format(idx, wan["vlan"], wan["spid"]))
        DEL_SPID = inp("Ingrese el SPID a eliminar")
        command(f"undo service-port {DEL_SPID}")
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha eliminado el SPID {DEL_SPID}",
                "info",
            )
        )
        return
    if action == "AS":
        if olt == "1":
            NEW_PLAN = inp("Ingrese el Nuevo Plan del cliente")
            serviceType = inp(
                """
    Ingrese el tipo de servicio a instalar :
    > I : Internet
    > V : VoIP
    > P : Publicas
    $ """
            )
            data["spid"] = spidCalc(data)[serviceType]
            log(f"SPID PARA AGG {data['spid']}, FUNCION AUN NO DISPONIBLE")
            return
        data["spid"] = availableSpid(comm,command)
        addOnuService(comm, command, data)
        verifySPID(comm,command,data)
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha Agregado el plan y vlan a {data['plan']} @ {data['vlan']}",
                "info",
            )
        )
        return
