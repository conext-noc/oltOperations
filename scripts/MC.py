from time import sleep
from helpers.clientFinder.dataLookup import dataLookup
from helpers.operations.addHandler import addOnuService
from helpers.operations.spid import availableSpid, spidCalc, verifySPID
from helpers.utils.display import display
from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.plans import oldPlans, plans
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
$ """
    )
    lookupType = inp("Buscar cliente por serial o por Datos (F/S/P/ID) [S | D] : ")
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
        modify(data["sn"],NEW_NAME,"NAME")
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
        modify(data["sn"],NEW_SN,"SN")
        quit()
        return
    if action == "CP":
        if olt != "1":
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
            modify(data["sn"],NEW_PLAN,"PLAN")
            modify(data["sn"],NEW_VLAN,"PROVIDER")
            quit()
            return
        NEW_PLAN = inp("Ingrese el Nuevo plana instalar : ")
        PLAN = plans[NEW_PLAN]
        """
        Apply a change to the srvProfile,Line Profile and gemport also deleting the existing spid
        
        steps:
        1. get the clients's spid
        2. delete the selected SPID
        3. modify clients srv and lp profiles
        4. generate a new spid with its specs
        5. reconfigure wan port
        """
        for wanData in data["wan"]:
            command(f"undo service-port {wanData['spid']}")
            
        command(f"interface gpon {data['frame']}/{data['slot']}")
        command(f"ont modify {data['port']} {data['id']} ont-lineprofile-id {PLAN['lineProfile']}")
        command(f"ont modify {data['port']} {data['id']} ont-srvprofile-id {PLAN['srvProfile']}")
        addVlan = inp("Se agregara vlan al puerto? [Y | N] : ")
        if addVlan == "Y":
            command(
                f" ont port native-vlan {data['port']} {data['id']} eth 1 vlan {PLAN['vlan']} "
            )
        command("quit")
        command(
        f' service-port {data["wan"][0]["spid"]} vlan {PLAN["vlan"]} gpon {data["frame"]}/{data["slot"]}/{data["port"]} ont {data["id"]} gemport {PLAN["gemPort"]} multi-service user-vlan {PLAN["vlan"]} tag-transform transparent inbound traffic-table index {PLAN["plan"]} outbound traffic-table index {PLAN["plan"]}'
        )
        sleep(10)
        command(f"interface gpon {data['frame']}/{data['slot']}")
        command(f"ont wan-config {data['port']} {data['id']} ip-index 2 profile-id 0")
        command("quit")
        return
    if action == "ES":
        log("| {:^3} | {:^4} | {:^6} |".format("IDX", "VLAN", "SPID"))
        for idx, wan in enumerate(data["wan"]):
            log("| {:^3} | {:^4} | {:^6} |".format(idx, wan["vlan"], wan["spid"]))
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
        if olt == "1":
            NEW_PLAN = inp("Ingrese el Nuevo Plan del cliente : ")
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
            quit()
            return
        data["wan"][0]["spid"] = availableSpid(comm,command)
        addOnuService(comm, command, data)
        verifySPID(comm,command,data)
        log(
            colorFormatter(
                f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha Agregado el plan y vlan a {data['plan']} @ {data['vlan']}",
                "info",
            )
        )
        quit()
        return
