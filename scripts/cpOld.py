from helpers.utils.printer import colorFormatter, inp, log
from helpers.info.plans import oldPlans
from helpers.operations.spid import verifySPID
from helpers.utils.sheets import modify


def dataPlanChanger(comm,command,quit,data):
    log("| {:^3} | {:^4} | {:^6} |".format("IDX", "VLAN", "SPID"))
    for idx, wan in enumerate(data["wan"]):
        log("| {:^3} | {:^4} | {:^6} |".format(
            idx, wan["vlan"], wan["spid"]))
    IDX = int(inp("Ingrese el INDEX del service-port a cambiar : "))
    NEW_PLAN = inp("Ingrese el Nuevo Plan del cliente : ")
    NEW_VLAN = inp("Ingrese la Nueva Vlan del cliente : ")
    command(f"undo service-port {data['wan'][IDX]['spid']}")
    PLAN_ID = oldPlans[data['olt']][NEW_PLAN]
    command(
        f" service-port {data['wan'][IDX]['spid']} vlan {NEW_VLAN} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['id']} gemport 14 multi-service user-vlan {NEW_VLAN} tag-transform transparent inbound traffic-table index {PLAN_ID} outbound traffic-table index {PLAN_ID}"
    )
    verifySPID(comm, command, data)
    log(
        colorFormatter(
            f"Al cliente {data['name']} {data['frame']}/{data['slot']}/{data['port']}/{data['id']} @ OLT {data['olt']} se le ha Cambiado el plan y vlan a {NEW_PLAN} @ {NEW_VLAN}",
            "info",
        )
    )
    modify(data["sn"], NEW_PLAN, "PLAN")
    modify(data["sn"], NEW_VLAN, "PROVIDER")
    quit()