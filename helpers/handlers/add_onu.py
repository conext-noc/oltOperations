from time import sleep
from helpers.handlers.printer import log, inp
from helpers.utils.decoder import decoder, check
from helpers.handlers.spid import calculate_spid
from helpers.handlers.fail import fail_checker
from helpers.constants.definitions import bridges

def add_client(comm, command, data):
    command(f"interface gpon {data['frame']}/{data['slot']}")
    sleep(3)
    command(
        f'ont add {data["port"]} sn-auth {data["sn"]} omci ont-lineprofile-id {data["line_profile"]} ont-srvprofile-id {data["srv_profile"]} desc "{data["name_1"]} {data["name_2"]} {data["contract"]}" '
    )
    sleep(7)
    value = decoder(comm)
    fail = fail_checker(value)
    if fail is not None:
        return (None, fail)
    (_, end) = check(value, "ONTID :").span()
    ID = value[end : end + 3].replace(" ", "").replace("\n", "").replace("\r", "")
    command(
        f'ont optical-alarm-profile {data["port"]} {ID} profile-name ALARMAS_OPTICAS'
    )
    command(f'ont alarm-policy {data["port"]} {ID} policy-name FAULT_ALARMS')
    command("quit")
    return (ID, fail)


def add_service(command, data):
    data["wan"][0]["spid"] = (
        calculate_spid(data)["I"]
        if "_IP" not in data["plan_name"]
        else calculate_spid(data)["P"]
    )

    log(f'El SPID que se le agregara al cliente es : {data["wan"][0]["spid"]}', "ok")

    command(f"interface gpon {data['frame']}/{data['slot']}")
    sleep(3)
    add_vlan = inp("Se agregara vlan al puerto? [Y | N] : ")

    command(
        f" ont port native-vlan {data['port']} {data['onu_id']} eth 1 vlan {data['wan'][0]['vlan']} "
    ) if add_vlan == "Y" else None

    IPADD = (
        inp("Ingrese la IPv4 Publica del cliente : ")
        if "_IP" in data["plan_name"]
        else None
    )

    sleep(3)
    
    internet_index = 2 if data['vendor'] != "BDCM" else 1
    
    command(
        f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 dhcp vlan {data['wan'][0]['vlan']}"
    ) if "_IP" not in data["plan_name"] and data['vendor'] != "BDCM" else command(
        f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 static ip-address {IPADD} mask 255.255.255.128 gateway 181.232.181.129 pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan 102"
    ) if "_IP" in data["plan_name"] and data['vendor'] != "BDCM" else command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 1 dhcp vlan {data['wan'][0]['vlan']} priority 0")
    sleep(3)

    if data['vendor'] == "BDCM":
        command(f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 dhcp vlan {data['wan'][0]['vlan']} priority 5")
    
    
    command(f"ont internet-config {data['port']} {data['onu_id']} ip-index {internet_index}")

    command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 2")

    command("quit")
    sleep(3)
    command(
        f"""service-port {data['wan'][0]['spid']} vlan {data['wan'][0]['vlan']} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['onu_id']} gemport {data["wan"][0]['gem_port']} multi-service user-vlan {data['wan'][0]['vlan']} tag-transform transparent inbound traffic-table index {data["wan"][0]["plan_idx"]} outbound traffic-table index {data["wan"][0]["plan_idx"]}"""
    )

    sleep(3)
    command(f"interface gpon {data['frame']}/{data['slot']}")
    sleep(3)
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 2 profile-id 0") if data['vendor'] != "BDCM" else command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 1 profile-id 0")
    sleep(3)
    if data['vendor'] == "BDCM":
        command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 2 profile-id 0")
        command(f"ont fec {data['port']} {data['onu_id']} use-profile-config")
        sleep(3)
    command("quit")


def add_service_mp(command, client, new_plan):
    log(f'El SPID que se le agregara al cliente es : {client["spid"]}', "ok")

    command(f"interface gpon {client['frame']}/{client['slot']}")
    sleep(3)

    command(
        f" ont port native-vlan {client['port']} {client['onu_id']} eth 1 vlan {new_plan['vlan']} "
    ) if client['device'] in bridges else None

    IPADD = (
        inp("Ingrese la IPv4 Publica del cliente : ")
        if "_IP" in new_plan["plan_name"]
        else None
    )

    sleep(3)
    
    internet_index = 2 if client['device'] != "BDCM" else 1
    
    command(
        f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 dhcp vlan {new_plan['vlan']}"
    ) if "_IP" not in client["plan_name"] and client['device'] != "BDCM" else command(
        f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 static ip-address {IPADD} mask 255.255.255.128 gateway 181.232.181.129 pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan 102"
    ) if "_IP" in new_plan["plan_name"] and client['device'] != "BDCM" else command(f"ont ipconfig {client['port']} {client['onu_id']} ip-index 1 dhcp vlan {new_plan['vlan']} priority 0")
    sleep(3)

    if client['device'] == "BDCM":
        command(f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 dhcp vlan {new_plan['vlan']} priority 5")
    
    
    command(f"ont internet-config {client['port']} {client['onu_id']} ip-index {internet_index}")

    command(f"ont policy-route-config {client['port']} {client['onu_id']} profile-id 2")

    command("quit")
    sleep(3)
    command(
        f"""service-port {client['spid']} vlan {new_plan['vlan']} gpon {client['frame']}/{client['slot']}/{client['port']} ont {client['onu_id']} gemport {new_plan['gem_port']} multi-service user-vlan {new_plan['vlan']} tag-transform transparent inbound traffic-table index {new_plan["plan_idx"]} outbound traffic-table index {new_plan["plan_idx"]}"""
    )

    sleep(3)
    command(f"interface gpon {client['frame']}/{client['slot']}")
    sleep(3)
    command(f"ont wan-config {client['port']} {client['onu_id']} ip-index 2 profile-id 0") if client['device'] != "BDCM" else command(f"ont wan-config {client['port']} {client['onu_id']} ip-index 1 profile-id 0")
    sleep(3)
    if client['device'] == "BDCM":
        command(f"ont wan-config {client['port']} {client['onu_id']} ip-index 2 profile-id 0")
        command(f"ont fec {client['port']} {client['onu_id']} use-profile-config")
        sleep(3)
    command("quit")
