import re
from time import sleep
from helpers.constants.definitions import (
    ONT_ROUTING_CONFIG,
    ONT_BRIDGING_CONFIG,
    BDCM_CONFIG,
    ROUTING_ONUS,
    endpoints,
)
from helpers.handlers.fail import fail_checker
from helpers.handlers.request import db_request
from helpers.handlers.spid import calculate_spid
from helpers.handlers.printer import log, inp
from helpers.utils.decoder import decoder


# Either user the next free index
# map the spid to the port
# use the same spid's <- selected✅
def clientsTable(comm, command, fsp, olt):
    FRAME = int(fsp.split("/")[0])
    SLOT = int(fsp.split("/")[1])
    PORT = int(fsp.split("/")[2])
    command(f"display ont info {FRAME} {SLOT} {PORT} all  | no-more")
    sleep(5)
    value = decoder(comm)
    fail = fail_checker(value)
    if fail != None:
        log(fail, "fail")
        return []
    ont_pattern = re.compile(r"(\d+/\s*\d+/\s*\d+)\s+(\d+)\s+(\w+)\s+(\w+)\s+(\w+)")
    description_pattern = re.compile(
        r"(\d+/\s*\d+/\s*\d+)\s+(\d+)\s+([A-Z0-9_\- ]+)", re.MULTILINE
    )

    # Extract ONT info
    ont_info = {}
    for match in ont_pattern.finditer(value):
        fsp = match.group(1).replace(" ", "")
        ont_id = match.group(2)
        ont_info[ont_id] = {
            "fsp": fsp,
            "ont_id": ont_id,
        }

    # Extract descriptions and add to ONT info
    for match in description_pattern.finditer(value):
        fsp = match.group(1).replace(" ", "")
        ont_id = match.group(2)
        description = match.group(3).strip()
        if ont_id in ont_info:
            ont_info[ont_id]["description"] = description

    return ont_info


def gather_onu_data(comm, command, slot, port, onu_id):
    command(f"display ont info 0 {slot} {port} {onu_id} | no-more")
    sleep(3)
    value = decoder(comm)
    fail = fail_checker(value)
    if fail != None:
        log(fail, "fail")
        return []
    sn_pattern = r"SN\s+:\s+([A-F0-9]+)"
    name_pattern = r"Description\s+:\s+([A-Za-z0-9_ -]+)"
    line_profile_id_pattern = r"Line profile ID\s+:\s+(\d+)"
    service_profile_id_pattern = r"Service profile ID\s+:\s+(\d+)"

    # Extracting the information using regex
    sn_match = re.search(sn_pattern, value)
    name_match = re.search(name_pattern, value)
    line_profile_id_match = re.search(line_profile_id_pattern, value)
    service_profile_id_match = re.search(service_profile_id_pattern, value)

    # Assigning the results to variables
    ont_sn = sn_match.group(1) if sn_match else None
    name = name_match.group(1).strip() if name_match else None
    line_profile_id = line_profile_id_match.group(1) if line_profile_id_match else None
    service_profile_id = (
        service_profile_id_match.group(1) if service_profile_id_match else None
    )
    spid_index = None
    vlan_id = None
    device = None
    device_db = ""
    traffic_table = None

    command(f"display service-port port 0/{slot}/{port} ont {onu_id} | no-more")
    sleep(3)
    spid_value = decoder(comm)
    pattern = r"\s+(\d+)\s+(\d+)\s+\w+\s+\w+\s+\d+/\d+\s*/\d+\s+\d+\s+\d+\s+\w+\s+\d+\s+(\d+)\s+\d+\s+\w+"
    fail = fail_checker(spid_value)
    if fail != None:
        log(fail, "fail")
        return []

    # Extracting the information using regex
    match = re.search(pattern, spid_value)

    # Assigning the results to variables
    if match:
        spid_index = match.group(1)
        vlan_id = match.group(2)
        traffic_table = match.group(3)

    command(f"display ont version 0 {slot} {port} {onu_id} | no-more")
    sleep(3)
    device_value = decoder(comm)
    device_pattern = r"Equipment-ID\s+:\s+([^\n]+)"
    fail = fail_checker(device_value)
    if fail != None:
        log(fail, "fail")
        return []

    # Extracting the information using regex
    match = re.search(device_pattern, device_value)

    # Assigning the results to variables
    if match:
        device = match.group(1)

    onu_db_data = db_request(
        endpoint=endpoints["get_client"],
        data={
            "lookup_type": "D",
            "lookup_value": {"olt": "*", "fspi": f"0/{slot}/{port}/{onu_id}"},
        },
    )

    if not onu_db_data["error"] and onu_db_data["data"] is not None:
        device_db = onu_db_data["data"]["device"]

    gem_port = 8 if int(vlan_id) in [1241, 2241] else 1

    return {
        "frame": 0,
        "slot": int(slot),
        "port": int(port),
        "id": int(onu_id),
        "name": name,
        "sn": ont_sn,
        "line_profile": int(line_profile_id),
        "srv_profile": int(service_profile_id),
        "spid": int(spid_index),
        "vlan": int(vlan_id),
        "traffic_table": int(traffic_table),
        "device": device.replace("\r", "").replace("\n", "").replace(" ", ""),
        "device_db": device_db.replace("\r", "").replace("\n", "").replace(" ", ""),
        "gem_port": int(gem_port),
    }


def migrate_onu(comm, command, slot, port, ont_list):
    for ont_id in ont_list.keys():
        onu_data = gather_onu_data(comm, command, slot=slot, port=port, onu_id=ont_id)
        dev = (
            onu_data["device"]
            if onu_data["device"] is not None
            else (
                onu_data["device_db"]
                if onu_data["device_db"] is not None
                else "EG8141V5"
            )
        )

        CONFIG = (
            ONT_ROUTING_CONFIG
            if dev in ROUTING_ONUS
            else BDCM_CONFIG if "1126" == dev else ONT_BRIDGING_CONFIG
        )

        if onu_data["vlan"] in [1104, 102]:
            print(
                f"""
!!!!!!!!!DEVICE NOT CHANGED!!!!!!!!!
PORT : {onu_data['frame']}/{onu_data['slot']}/{onu_data['port']}/{onu_data['id']})
ONT SN: {onu_data['sn']}
Name: {onu_data['name']}
Line Profile ID: {onu_data['line_profile']}
Service Profile ID: {onu_data['service_profile']}
SPID: {onu_data['spid']}
VLAN: {onu_data['vlan']}
TRAFFIC TABLE ID: {onu_data['traffic_table']}
DEVICE: {dev}
\n""",
                file=open("progress_missing.log", "a"),
            )
            continue
        else:
            print(
                f"undo service-port {onu_data['spid']}",
                file=open("progress_commands.log", "a"),
            )
            command(f"undo service-port {onu_data['spid']}")
            sleep(2)
            print(
                f"interface gpon {onu_data['frame']}/{onu_data['slot']}",
                file=open("progress_commands.log", "a"),
            )
            command(f"interface gpon {onu_data['frame']}/{onu_data['slot']}")
            sleep(2)
            print(
                f"ont delete {onu_data['port']} {onu_data['id']}",
                file=open("progress_commands.log", "a"),
            )
            command(f"ont delete {onu_data['port']} {onu_data['id']}")
            sleep(2)
            for line in iter(CONFIG.splitlines()):
                print(line.format(**onu_data), file=open("progress_commands.log", "a"))
                command(line.format(**onu_data))
                sleep(2)
            print("\n", file=open("progress_commands.log", "a"))
            print(
                f"""
PORT : {onu_data['frame']}/{onu_data['slot']}/{onu_data['port']}/{onu_data['id']})
ONT SN: {onu_data['sn']}
Name: {onu_data['name']}
Line Profile ID: {onu_data['line_profile']}
Service Profile ID: {onu_data['srv_profile']}
SPID: {onu_data['spid']}
VLAN: {onu_data['vlan']}
TRAFFIC TABLE ID: {onu_data['traffic_table']}
DEVICE: {dev}
\n""",
                file=open("progress.log", "a"),
            )


def migration(comm, command, quit_ssh, device,*args, **kwargs):
    action = inp("Desea realizar la migracion en toda la OLT? [Y/N] : ")
    if action == "Y":
        for slot in range(1, 16):
            if slot == 8 or slot == 9:
                continue
            else:
                for port in range(0, 15):
                    print(f"PORT : 0/{slot}/{port}")
                    print(f"PORT : 0/{slot}/{port}", file=open("progress.log", "a"))
                    ont_list = clientsTable(comm, command, f"0/{slot}/{port}", device)
                    migrate_onu(comm, command, slot=slot, port=port, ont_list=ont_list)
    else:
        slot = inp("Ingrese la tarjeta del ONT : ")
        port = inp("Ingrese el puerto del ONT : ")
        onu_count = inp("Ingrese la cantidad de ont a migrar : ")
        onu_list = {}
        for onu in range(onu_count):
            onu_id = inp(f"Ingrese el ID del ONT {onu} : ")
            onu_list[onu_id] = {
                "fsp": f"0/{slot}/{port}",
                "ont_id": onu_id,
            }
        migrate_onu(comm, command, slot=slot, port=port, ont_list=onu_list)
    quit_ssh()
