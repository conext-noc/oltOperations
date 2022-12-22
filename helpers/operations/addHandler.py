from helpers.clientFinder.wanInterface import preWan
from helpers.utils.decoder import decoder, check
from helpers.failHandler.fail import failChecker
from helpers.utils.printer import inp
from helpers.info.plans import oldPlans


def addONU(comm, command, data):
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(
        f'ont add {data["port"]} sn-auth {data["sn"]} omci ont-lineprofile-name "{data["lineProfile"]}" ont-srvprofile-name "{data["srvProfile"]}"  desc "{data["name"]}" '
    )
    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        (_, end) = check(value, "ONTID :").span()
        ID = value[end : end + 3].replace(" ", "").replace("\n", "")
        command(
            f'ont optical-alarm-profile {data["port"]} {data["id"]} profile-name ALARMAS_OPTICAS'
        )
        command(
            f'ont alarm-policy {data["port"]} {data["id"]} policy-name FAULT_ALARMS'
        )
        command("quit")
        return (ID, fail)
    else:
        return (None, fail)


def addOnuService(comm, command, data):
    preg = inp(
        "Desea verificar si el cliente ya tiene la wan interface configurada? [Y | N] : "
    ).upper()
    if preg == "Y":
        preWan(comm, command, data)
        
    data["wan"][0]["vlan"] = inp("Ingrese la vlan de proveedor de cliente : ")
    data["wan"][0]["plan"] = inp("Ingrese plan de cliente : ")

    addVlan = inp("Se agregara vlan al puerto? [Y | N] : ").upper()

    if addVlan == "Y":
        command(f"interface gpon {data['frame']}/{data['slot']}")
        command(
            f" ont port native-vlan {data['port']} {data['id']} eth 1 vlan {data['wan'][0]['vlan']} "
        )
        command("quit")
    PLAN_ID = oldPlans[data['olt']][data['wan'][0]['plan']]
    command(
        f' service-port {data["wan"][0]["spid"]} vlan {data["wan"][0]["vlan"]} gpon {data["frame"]}/{data["slot"]}/{data["port"]} ont {data["id"]} gemport 14 multi-service user-vlan {data["wan"][0]["vlan"]} tag-transform transparent inbound traffic-table index {PLAN_ID} outbound traffic-table index {PLAN_ID}'
    )
