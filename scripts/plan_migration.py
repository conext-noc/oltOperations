import re
from time import sleep
from helpers.constants.definitions import (
    ONT_ROUTING_CONFIG,
    ONT_BRIDGING_CONFIG,
    BDCM_CONFIG,
    ROUTING_ONUS,
    endpoints,
    map_ports
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


def gather_onu_data(comm, command, slot, port, onu_id, olt):
    command(f"display ont info 0 {slot} {port} {onu_id} | no-more")
    sleep(5)
    value = decoder(comm)
    fail = fail_checker(value)
    if fail != None:
        log(fail, "fail")
        return []
    sn_pattern = r"SN\s+:\s+([A-F0-9]+)"
    name_pattern = r"Description\s+:\s+([A-Za-z0-9_ -]+)"

    # Extracting the information using regex
    sn_match = re.search(sn_pattern, value)
    name_match = re.search(name_pattern, value)

    # Assigning the results to variables
    ont_sn = sn_match.group(1) if sn_match else None
    name = name_match.group(1).strip() if name_match else None
    spid_index = calculate_spid({"slot": slot, "port": port, "onu_id": onu_id})["I"]
    device = "EG8141V5"

    command(f"display ont version 0 {slot} {port} {onu_id} | no-more")
    sleep(5)
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
            "lookup_value": {"olt": olt, "fspi": f"0/{slot}/{port}/{onu_id}"},
        },
    )
    data_plans = db_request(endpoints["get_plans"], {})["data"]
    new_plan = [
        data_plan for data_plan in data_plans if onu_db_data["data"]["plan_name"] == data_plan["plan_name"]
    ][0]

    if not onu_db_data["error"] and onu_db_data["data"] is not None:
        device_db = onu_db_data["data"]["device"]

    gem_port = 8 if int(new_plan['vlan']) in [1241, 2241] else 1

    return {
        "frame": 0,
        "slot": int(slot),
        "port": int(port),
        "id": int(onu_id),
        "name": name,
        "sn": ont_sn,
        "line_profile": int(new_plan['line_profile']),
        "srv_profile": int(new_plan['srv_profile']),
        "spid": int(spid_index),
        "vlan": int(new_plan['vlan']),
        "traffic_table": int(new_plan["plan_idx"]),
        "device": device.replace("\r", "").replace("\n", "").replace(" ", ""),
        "device_db": device_db.replace("\r", "").replace("\n", "").replace(" ", ""),
        "gem_port": int(gem_port),
    }


def migrate_onu(comm, command, slot, port, ont_list, olt):
    for ont_id in ont_list.keys():
        onu_data = gather_onu_data(comm, command, slot=slot, port=port, onu_id=ont_id, olt=olt)
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
Service Profile ID: {onu_data['srv_profile']}
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


def migration(comm, command, quit_ssh, device, *args, **kwargs):
    initializin = False
    action = inp("Desea realizar la migracion en toda la OLT? [Y/N] : ")

    fsp = input("""Escribe el FSP desde donde iniciar [F/S/P]:  """)

    map_ports_keys = map_ports.items()
    
    if action == "Y":
        for clave, valor in map_ports_keys:
            if valor == fsp or initializin == True:
                initializin=True
                slot = valor.split("/")[1]
                port = valor.split("/")[2]
                print(f"PORT : 0/{slot}/{port}")
                print(f"PORT : 0/{slot}/{port}", file=open("progress.log", "a"))
                ont_list = clientsTable(comm, command, f"0/{slot}/{port}", device)
                migrate_onu(comm, command, slot=slot, port=port, ont_list=ont_list, olt=device)
    else:
        slot = inp("Ingrese la tarjeta del ONT : ")
        port = inp("Ingrese el puerto del ONT : ")
        onu_count = int(inp("Ingrese la cantidad de ont a migrar : ") or 0)
        onu_list = {}
        for onu in range(onu_count):
            onu_id = inp(f"Ingrese el ID del ONT {onu} : ")
            onu_list[onu_id] = {
                "fsp": f"0/{slot}/{port}",
                "ont_id": onu_id,
            }
        migrate_onu(comm, command, slot=slot, port=port, ont_list=onu_list,olt=device)
    quit_ssh()
