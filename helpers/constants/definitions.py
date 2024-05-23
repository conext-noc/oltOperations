import json
from os import device_encoding, getcwd
from typing import Dict, List, Union, Optional
import dataclasses

@dataclasses.dataclass
class AvailableOnu:
    frame: int
    slot: int
    port: int
    olt: int
    fsp: str
    sn: str
    device: str


@dataclasses.dataclass
class OnuLookup:
    slot: int
    port: int
    olt: int
    external_id: Optional[str] = "-"


@dataclasses.dataclass
class OnuDeactivatedResponse:
    frame: 0
    slot: int
    port: int
    onu_id: int
    olt: int
    state: str
    zone: str
    sn: str


@dataclasses.dataclass
class OnuAlarmResponse:
    frame: 0
    slot: int
    port: int
    onu_id: int
    olt: int
    status: str
    date: str
    zone: str
    sn: str


@dataclasses.dataclass
class InstallRequest:
    contract: str
    name: str
    pon: str
    olt: int
    sn: str
    slot: int
    port: int
    device: str
    plan: str
    profile: str
    address: str
    vlan: int
    fsp: str
    mode: str
    temp: float
    power: float
    frame: 0
    odb: Optional[str] = "Splitter1"
    latitude: Optional[float] = 10.653860
    longitude: Optional[float] = -71.645966
    
    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self), indent=4)

@dataclasses.dataclass
class Client:
    name: str
    pon: str
    olt: int
    sn: str
    frame: 0
    slot: int
    port: int
    onu_id: int
    device: str
    # profile: str
    address: str
    vlan: int
    mode: str
    zone: str
    power: float
    status: str
    state: str
    has_tr069: bool = False
    temp: Optional[float] = 25.0
    contract: Optional[str] = ""
    plan: Optional[str] = ""
    odb: Optional[str] = "CP1-FDT1-DB1-FAT1"
    latitude: Optional[float] = 10.653860
    longitude: Optional[float] = -71.645966


@dataclasses.dataclass
class Onu:
    device: str
    mode: str


@dataclasses.dataclass
class StaticIp:
    sn: str
    contract: str
    ip: str
    mask: str
    vlan: int


@dataclasses.dataclass
class Plan:
    profile: str
    name: str
    line_profile: str
    srv_profile: str
    gem_port: int
    vlan: int
    traffic_table: int


@dataclasses.dataclass
class Zone:
    name: str
    zone_id: int


@dataclasses.dataclass
class ODB:
    name: str
    zone_id: int
    odb_id: int
    ports: int
    latitude: float = 10.653860
    longitude: float = -71.645966

CONF_FILES = f"{getcwd()}/configs"

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
