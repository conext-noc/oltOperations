from time import sleep
from helpers.clientFinder.wan import wan
from helpers.operations.spid import spidCalc
from helpers.utils.decoder import decoder, check
from helpers.failHandler.fail import failChecker
from helpers.utils.printer import colorFormatter, inp, log


def addONUNew(comm, command, data):
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(
        f'ont add {data["port"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["lineProfile"]} ont-srvprofile-id {data["srvProfile"]} desc "{data["name"]}" '
    )
    value = decoder(comm)
    fail = failChecker(value)
    if fail == None:
        (_, end) = check(value, "ONTID :").span()
        ID = value[end : end + 3].replace(" ", "").replace("\n", "").replace("\r", "")
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


def addOnuServiceNew(comm, command, data):
    serviceType = inp(
        """
    Ingrese el tipo de servicio a instalar :
    > I : Internet
    > V : VoIP
    > P : Publicas
    $ """
    )
    data["wan"][0]["spid"] = spidCalc(data)[serviceType]

    log(
        colorFormatter(
            f'El SPID que se le agregara al cliente es : {data["wan"][0]["spid"]}', "ok"
        )
    )

    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(
        f"ont ipconfig {data['port']} {data['id']} ip-index 2 dhcp vlan {data['wan'][0]['vlan']}"
    )
    command(f"ont internet-config {data['port']} {data['id']} ip-index 2")
    command(f"ont policy-route-config {data['port']} {data['id']} profile-id 2")
    
    addVlan = inp("Se agregara vlan al puerto? [Y | N] : ")
    if addVlan == "Y":
        command(
            f" ont port native-vlan {data['port']} {data['id']} eth 1 vlan {data['wan'][0]['vlan']} "
        )
    command("quit")

    command(
        f' service-port {data["spid"]} vlan {data["wan"][0]["vlan"]} gpon {data["frame"]}/{data["slot"]}/{data["port"]} ont {data["id"]} gemport {data["gemPort"]} multi-service user-vlan {data["wan"][0]["vlan"]} tag-transform transparent inbound traffic-table index {data["wan"][0]["plan"]} outbound traffic-table index {data["wan"][0]["plan"]}'
    )
    IPADDRESS = None
    while IPADDRESS == None:
        (IPADDRESS, _) = wan(comm, command, data['frame'], data['slot'], data['port'], data['id'], data['olt'])
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"ont wan-config {data['port']} {data['id']} ip-index 2 profile-id 0")
    command("quit")
