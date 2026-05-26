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
        if not data.get("is_ip") and "_IP" not in data["plan_name"]
        else calculate_spid(data)["P"]
    )
    
    log(f'El SPID que se le agregara al cliente es : {data["wan"][0]["spid"]}', "ok")

    command(f"interface gpon {data['frame']}/{data['slot']}")
    sleep(3)

    install_mode = inp("Se instalara en modo Bridge o Router? [B | R] : ").upper()

    IPADD = (
        inp("Ingrese la IPv4 Publica del cliente : ")
        if data.get("is_ip") or "_IP" in data["plan_name"]
        else None
    )
    IPGW = (
        inp("Ingrese la IPv4 del Gateway del cliente : ")
        if data.get("is_ip") or "_IP" in data["plan_name"]
        else None
    )
    IPVLAN = (
        inp("Ingrese la VLAN del Gateway del cliente : ")
        if data.get("is_ip") or "_IP" in data["plan_name"]
        else None
    )

    if IPVLAN:
        data["wan"][0]["vlan"] = IPVLAN

    internet_conf = ""
    ip_index = 2 if data["device"] != "BDCM" else 1
    ip_priority = 5 if data["device"] != "BDCM" else 0
    
    if IPADD is None:
        if install_mode == "B":
            internet_conf = (
                f"dhcp vlan {data['wan'][0]['vlan']} priority {ip_priority}"
            )
        else:
            internet_conf = (
                f"ip-index {ip_index} dhcp vlan {data['wan'][0]['vlan']} priority {ip_priority}"
            )
    else:
        if install_mode == "B":
            internet_conf = f"static ip-address {IPADD} mask 255.255.255.128 gateway {IPGW} pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan {data['wan'][0]['vlan']}"
        else:
            internet_conf = f"ip-index {ip_index} static ip-address {IPADD} mask 255.255.255.128 gateway {IPGW} pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan {data['wan'][0]['vlan']}"
        
    
    sleep(1)
    command(f"ont ipconfig {data['port']} {data['onu_id']} {internet_conf}")
    sleep(1)

    if install_mode == "R":
        command(f"ont wan-config {data['port']} {data['onu_id']} ip-index {ip_index} profile-id 0")
        sleep(1)
        command(f"ont internet-config {data['port']} {data['onu_id']} ip-index {ip_index}")
        sleep(1)

    command(f"ont policy-route-config {data['port']} {data['onu_id']} profile-id 2")
    sleep(1)
    command(f"ont fec {data['port']} {data['onu_id']} use-profile-config")

    if install_mode == "R" and data["device"] == "BDCM":
        command(
            f"ont ipconfig {data['port']} {data['onu_id']} ip-index 2 dhcp vlan {data['wan'][0]['vlan']} priority 5"
        )
        sleep(1)
        command(
            f"ont wan-config {data['port']} {data['onu_id']} ip-index 1 profile-id 0"
        )
        sleep(1)
        command(f"ont internet-config {data['port']} {data['onu_id']} ip-index 1")

    if install_mode == "B":
        sleep(1)
        command(f"ont port native-vlan {data['port']} {data['onu_id']} eth 1 vlan {data['wan'][0]['vlan']} priority 0")
        sleep(1)
        command(f"ont port native-vlan {data['port']} {data['onu_id']} eth 2 vlan {data['wan'][0]['vlan']} priority 0")
        sleep(1)
        command(f"ont port native-vlan {data['port']} {data['onu_id']} eth 3 vlan {data['wan'][0]['vlan']} priority 0")
        sleep(1)
        command(f"ont port native-vlan {data['port']} {data['onu_id']} eth 4 vlan {data['wan'][0]['vlan']} priority 0")
        sleep(1)

    # per device custom config
    if install_mode == "B" and data["device"] == "EG8120L" and data.get("software") == "V3R017C10S120":
        sleep(1)
        command(f"ont port route {data['port']} {data['onu_id']} eth 1 disable")
        sleep(1)
        command(f"ont port route {data['port']} {data['onu_id']} eth 2 disable")

    if install_mode == "R" and data["device"] != "BDCM":
        sleep(1)
        command(f"ont port route {data['port']} {data['onu_id']} eth 1 enable")
        sleep(1)
        command(f"ont port route {data['port']} {data['onu_id']} eth 2 enable")
        sleep(1)
        command(f"ont port route {data['port']} {data['onu_id']} eth 3 enable")
        sleep(1)
        command(f"ont port route {data['port']} {data['onu_id']} eth 4 enable")


    command("quit")

    sleep(3)
    command(
        f"""service-port {data["wan"][0]["spid"]} vlan {data['wan'][0]['vlan']} gpon {data['frame']}/{data['slot']}/{data['port']} ont {data['onu_id']} gemport {data['wan'][0]['gem_port']} multi-service user-vlan {data['wan'][0]['vlan']} tag-transform transparent inbound traffic-table index {data['wan'][0]["plan_idx"]} outbound traffic-table index {data["wan"][0]["plan_idx"]}"""
    )
    sleep(5)
    command(f"interface gpon {data['frame']}/{data['slot']}")
    command(f"ont wan-config {data['port']} {data['onu_id']} ip-index 2 profile-id 0")
    command("quit")

def add_service_mp(command, client, new_plan):
    log(f'El SPID que se le agregara al cliente es : {client["spid"]}', "ok")

    command(f"interface gpon {client['frame']}/{client['slot']}")
    sleep(3)

    install_mode = inp("Se instalara en modo Bridge o Router? [B | R] : ").upper()

    IPADD = (
        inp("Ingrese la IPv4 Publica del cliente : ")
        if new_plan.get("is_ip") or "_IP" in new_plan["plan_name"]
        else None
    )
    IPGW = (
        inp("Ingrese la IPv4 del Gateway del cliente : ")
        if new_plan.get("is_ip") or "_IP" in new_plan["plan_name"]
        else None
    )
    IPVLAN = (
        inp("Ingrese la VLAN del Gateway del cliente : ")
        if new_plan.get("is_ip") or "_IP" in new_plan["plan_name"]
        else None
    )

    if IPVLAN:
        new_plan['vlan'] = IPVLAN

    # base config
    command(f"ont fec {client['port']} {client['onu_id']} use-profile-config")
    command(f"ont policy-route-config {client['port']} {client['onu_id']} profile-id 2")
    
    if install_mode == "R":
        command(
            f"ont wan-config {client['port']} {client['onu_id']} ip-index 2 profile-id 0"
        )
        command(f"ont internet-config {client['port']} {client['onu_id']} ip-index 2")

    if install_mode == "B":
        command(f"ont port native-vlan {client['port']} {client['onu_id']} eth 1 vlan {new_plan['vlan']} priority 0")
        command(f"ont port native-vlan {client['port']} {client['onu_id']} eth 2 vlan {new_plan['vlan']} priority 0")
        command(f"ont port native-vlan {client['port']} {client['onu_id']} eth 3 vlan {new_plan['vlan']} priority 0")
        command(f"ont port native-vlan {client['port']} {client['onu_id']} eth 4 vlan {new_plan['vlan']} priority 0")

    internet_conf = ""
    ip_index = 2 if client["device"] != "BDCM" else 1
    ip_priority = 5 if client["device"] != "BDCM" else 0

    if IPADD is None:
        if install_mode == "B":
            internet_conf = (
                f"dhcp vlan {new_plan['vlan']} priority {ip_priority}"
            )
        else:
            internet_conf = (
                f"ip-index {ip_index} dhcp vlan {new_plan['vlan']} priority {ip_priority}"
            )
    else:
        if install_mode == "B":
            internet_conf = f"static ip-address {IPADD} mask 255.255.255.128 gateway {IPGW} pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan {new_plan['vlan']}"
        else:
            internet_conf = f"ip-index {ip_index} static ip-address {IPADD} mask 255.255.255.128 gateway {IPGW} pri-dns 9.9.9.9 slave-dns 149.112.112.112 vlan {new_plan['vlan']}"

    # per device custom config
    if install_mode == "B" and client["device"] == "EG8120L":
        command(f"ont port route {client['port']} {client['onu_id']} eth 1 disable")
        command(f"ont port route {client['port']} {client['onu_id']} eth 2 disable")

    if install_mode == "R" and client["device"] != "BDCM":
        command(f"ont port route {client['port']} {client['onu_id']} eth 1 enable")
        command(f"ont port route {client['port']} {client['onu_id']} eth 2 enable")
        command(f"ont port route {client['port']} {client['onu_id']} eth 3 enable")
        command(f"ont port route {client['port']} {client['onu_id']} eth 4 enable")

    if install_mode == "R" and client["device"] == "BDCM":
        command(
            f"ont wan-config {client['port']} {client['onu_id']} ip-index 1 profile-id 0"
        )
        command(f"ont internet-config {client['port']} {client['onu_id']} ip-index 1")
        command(
            f"ont ipconfig {client['port']} {client['onu_id']} ip-index 2 dhcp vlan {new_plan['vlan']} priority 5"
        )

    command(f"ont ipconfig {client['port']} {client['onu_id']} {internet_conf}")
    command("quit")

    command(
        f"""service-port {client['spid']} vlan {new_plan['vlan']} gpon {client['frame']}/{client['slot']}/{client['port']} ont {client['onu_id']} gemport {new_plan['gem_port']} multi-service user-vlan {new_plan['vlan']} tag-transform transparent inbound traffic-table index {new_plan["plan_idx"]} outbound traffic-table index {new_plan["plan_idx"]}"""
    )
