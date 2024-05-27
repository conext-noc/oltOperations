from typing import Dict, List, Union, Optional
import dataclasses

@dataclasses.dataclass
class Client:
    """General Class for client data
    """
    contract: str
    name_1: str
    name_2: str
    frame: int
    slot: int
    port: int
    onu_id: int
    olt: int
    fsp: str
    fspi: str
    status: str
    state: str
    vlan: int
    plan_name: str
    provider: str
    device: str
    sn: str
    vendor: str
    last_down_cause: str
    last_down_time: str
    last_down_date: str
    temperature: float
    rx_power: float
    tx_power: float
    line_profile: str
    srv_profile: str
    spid: int

@dataclasses.dataclass
class ClientRequest:
    contract: str
    frame: Optional[int] = 0
    slot: Optional[int] = 1
    port: Optional[int] = 0
    onu_id: Optional[int] = 0
    olt: Optional[int] = 1
    fsp: Optional[str] = "0/1/0"
    fspi: Optional[str] = "0/1/0/0"
    sn: Optional[str] = "48575443ABCD1234"

headers = {"Content-Type": "application/json"}
# domain = "http://127.0.0.1:8000"
domain = "http://db-api.conext.net.ve"
payload = {"lookup_type": None, "lookup_value": None}
payload_add = {"data": None}
endpoints = {
    "add_client": "/add-client",
    "get_client": "/get-client",
    "get_clients": "/get-clients",
    "update_client": "/update-client",
    "remove_client": "/remove-client",
    "get_plans": "/get-plans",
    "add_ports": "/add-ports",
    "get_ports": "/get-ports",
    "open_ports": "/open-ports",
    "disable_ports": "/disable-ports",
    "get_alarms": "/get-alarms",
    "add_alarms": "/add-alarms",
    "empty_alarms": "/empty-alarms",
    "ms_health_check": "/ms-health-check",
    "populate": "/populate",
    "get_creds": "/get-creds",
    "get_acls": "/get-acls",
    "create_acls": "/create-acls",
}
olt_devices = {"1": "181.232.180.7", "2": "181.232.180.5", "3": "181.232.180.6"}
rtr_devices = {
    "E1": "181.232.180.1",
    "E2": "181.232.180.2",
    "A1": "181.232.180.3",
    "A2": "181.232.180.4",
}
rtrs = ["A1", "A2", "E1", "E2"]
olts = ["1", "2", "3"]
client_place_holder = {
    "fail": None,
    "name_1": None,
    "name_2": None,
    "contract": None,
    "olt": None,
    "frame": None,
    "slot": None,
    "port": None,
    "onu_id": None,
    "fsp": None,
    "fspi": None,
    "sn": None,
    "last_down_cause": None,
    "state": None,
    "status": None,
    "type": None,
    "vendor": None,
    "ip_address": None,
    "plan_name": None,
    "spid": None,
    "vlan": None,
    "plan": None,
    "provider": None,
    "plan_name": None,
    "temp": None,
    "pwr": None,
    "line_profile": None,
    "srv_profile": None,
    "device": None,
    "wan": [{"vlan": None, "spid": None, "plan_name": None, "provider": None}],
}

client_payload = {
    "frame": None,
    "slot": None,
    "port": None,
    "onu_id": None,
    "olt": None,
    "fsp": None,
    "fspi": None,
    "name_1": None,
    "name_2": None,
    "contract": None,
    "status": None,
    "state": None,
    "sn": None,
    "device": None,
    "plan_name": None,
    "spid": None,
}

change_types = ["CT", "CP", "CO"]

bridges = ["EG8120L", "EG8010Hv6", "010H"]

############################# OIDS & SNMP #############################

snmp_oid = {
    "descr": "1.3.6.1.4.1.2011.6.128.1.1.2.43.1.9",
    "serial": ".1.3.6.1.4.1.2011.6.128.1.1.2.43.1.3",
    "power": "1.3.6.1.4.1.2011.6.128.1.1.2.51.1.4",
    "ldc": "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.24",
    "lddt": "1.3.6.1.4.1.2011.6.128.1.1.2.46.1.23",
    "status": ".1.3.6.1.4.1.2011.6.128.1.1.2.46.1.15",
    "device":"1.3.6.1.4.1.2011.6.128.1.1.2.45.1.4",
    "ip_addr":"1.3.6.1.4.1.2011.6.128.1.1.2.49.1.2",
    "state":"1.3.6.1.4.1.2011.6.128.1.1.2.46.1.1",
    "srv_prof":"1.3.6.1.4.1.2011.6.128.1.1.2.43.1.8",
    "lin_prof":"1.3.6.1.4.1.2011.6.128.1.1.2.43.1.7",
    "vlan":"1.3.6.1.4.1.2011.5.110.1.10.1.4",
    
}


snmp_down_causes = {
    "1": "LOS(Loss of signal)",
    "2": "LOSi(Loss of signal for ONUi) or LOBi (Loss of burst for ONUi)",
    "3": "LOFI(Loss of frame of ONUi)",
    "4": "SFI(Signal fail of ONUi)",
    "5": "LOAI(Loss of acknowledge with ONUi)",
    "6": "LOAMI(Loss of PLOAM for ONUi)",
    "7": "deactive ONT fails",
    "8": "deactive ONT success",
    "9": "reset ONT",
    "10": "re-register ONT",
    "11": "pop up fail",
    "13": "dying-gasp",
    "15": "LOKI(Loss of key synch with ONUi)",
    "18": "deactived ONT due to the ring",
    "30": "shut down ONT optical module",
    "31": "reset ONT by ONT command",
    "32": "reset ONT by ONT reset button",
    "33": "reset ONT by ONT software",
    "34": "deactived ONT due to broadcast attack",
    "35": "operator check fail",
    "37": "a rogue ONT detected by itself",
    "-1": "indicates that the query fails.",
}

snmp_status_types = {"1": "online", "2": "offline"}
snmp_state_types = {"1": "activate", "2": "deactivate"}

ONT_ROUTING_CONFIG = """
 interface gpon 0/{slot}
 ont add {port} {id} sn-auth "{sn}" omci ont-lineprofile-id {line_profile} ont-srvprofile-id {srv_profile} desc "{name}"
 ont optical-alarm-profile {port} {id} profile-id 3
 ont alarm-policy {port} {id} policy-id 1
 ont ipconfig {port} {id} ip-index 1 dhcp vlan {vlan} priority 0
 ont internet-config {port} {id} ip-index 1
 ont wan-config {port} {id} ip-index 1 profile-id 0
 ont policy-route-config {port} {id} profile-id 0
 ont fec {port} {id} use-profile-config
 ont port route {port} {id} eth 1 enable
 ont port route {port} {id} eth 2 enable
 ont port route {port} {id} eth 3 enable
 ont port route {port} {id} eth 4 enable
 ont port route {port} {id} eth 5 enable
 ont port route {port} {id} eth 6 enable
 ont port route {port} {id} eth 7 enable
 ont port route {port} {id} eth 8 enable
quit
service-port {spid} vlan {vlan} gpon 0/{slot}/{port} ont {id} gemport {gem_port} multi-service user-vlan {vlan} tag-transform transparent inbound traffic-table index {traffic_table} outbound traffic-table index {traffic_table}"""

ONT_BRIDGING_CONFIG = """
interface gpon 0/{slot}
 ont add {port} {id} sn-auth "{sn}" omci ont-lineprofile-id {line_profile} ont-srvprofile-id {srv_profile} desc "{name}"
 ont optical-alarm-profile {port} {id} profile-id 3
 ont alarm-policy {port} {id} policy-id 1
 ont fec {port} {id} use-profile-config
 ont port native-vlan {port} {id} eth 1 vlan {vlan} priority 0
 ont port native-vlan {port} {id} eth 2 vlan {vlan} priority 0
 ont port native-vlan {port} {id} eth 3 vlan {vlan} priority 0
 ont port native-vlan {port} {id} eth 4 vlan {vlan} priority 0
 ont port native-vlan {port} {id} eth 5 vlan {vlan} priority 0
 ont port native-vlan {port} {id} eth 6 vlan {vlan} priority 0
 ont port native-vlan {port} {id} eth 7 vlan {vlan} priority 0
 ont port native-vlan {port} {id} eth 8 vlan {vlan} priority 0
quit
service-port {spid} vlan {vlan} gpon 0/{slot}/{port} ont {id} gemport {gem_port} multi-service user-vlan {vlan} tag-transform transparent inbound traffic-table index {traffic_table} outbound traffic-table index {traffic_table}"""

# HG81126
BDCM_CONFIG = """
interface gpon 0/{slot}
 ont add {port} {id} sn-auth "{sn}" omci ont-lineprofile-id {line_profile} ont-srvprofile-id {srv_profile} desc "{name}"
 ont optical-alarm-profile {port} {id} profile-id 3
 ont alarm-policy {port} {id} policy-id 1
 ont ipconfig {port} {id} ip-index 1 dhcp vlan {vlan} priority 0
 ont ipconfig {port} {id} ip-index 2 dhcp vlan {vlan} priority 5
 ont wan-config {port} {id} ip-index 2 profile-id 0
 ont wan-config {port} {id} ip-index 1 profile-id 0
 ont internet-config {port} {id} ip-index 2
 ont internet-config {port} {id} ip-index 1
 ont policy-route-config {port} {id} profile-id 2
 ont fec {port} {id} use-profile-config
quit
service-port {spid} vlan {vlan} gpon 0/{slot}/{port} ont {id} gemport {gem_port} multi-service user-vlan {vlan} tag-transform transparent inbound traffic-table index {traffic_table} outbound traffic-table index {traffic_table}"""

ROUTING_ONUS = ["EG8141A5","EG8145V5", "EG8145X6","HG8321R", "HG8546M", "HS8145V","HS8546V5"]
BDCM_ONU = "HG81126"
