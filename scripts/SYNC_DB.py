import re
from itertools import zip_longest
from time import sleep
from helpers.constants.definitions import endpoints, payload
from helpers.utils.decoder import check_iter, decoder
from helpers.handlers.request import db_request
from helpers.handlers.fail import fail_checker
from helpers.handlers.printer import log
from helpers.handlers.file_formatter import data_to_dict
from helpers.utils.ssh import ssh

def clientsTable(comm, command, fsp, olt):
    CLIENTS = []
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
    ont_info_pattern = re.compile(
        r'(\d+/\s*\d+/\d+)\s+(\d+)\s+([A-F0-9]+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)\s+(\w+)'
    )
    
    ont_info_matches = ont_info_pattern.findall(value)
    ont_info_list = [
        {
            "F/S/P": match[0],
            "ONT ID": match[1],
            "SN": match[2],
            "Control flag": match[3],
            "Run state": match[4],
            "Config state": match[5],
            "Match state": match[6],
            "Protect side": match[7]
        }
        for match in ont_info_matches
    ]
    
    for client_info in ont_info_list:
        CLIENTS.append({
        "fspi": f"{client_info['F/S/P'].replace(' ','')}/{client_info['ONT ID']}",
        "onu_id": int(client_info['ONT ID']),
        "fsp": f"{client_info['F/S/P'].replace(' ','')}",
        "olt": int(olt),
        "sn": client_info["SN"],
        "state": client_info["Control flag"]
    })
    log(f"{fsp} done", "success")
    return CLIENTS

def db_sync(comm,command, quit_ssh, olt, action):
    for slot in range(1,16):
        if slot == 8 or slot == 9:
            continue
        else:
            for port in range(0,15):
                clients = clientsTable(comm, command, f"0/{slot}/{port}", olt)
                payload["lookup_type"] = "VP"
                payload["lookup_value"] = {"fsp":f"0/{slot}/{port}", "olt":olt}
                response = db_request(endpoints["get_clients"], payload)["data"]
                zipped_lists = list(zip_longest(clients, response, fillvalue=None))
                for olt_client,db_client in zipped_lists:
                    if olt_client is None or db_client is None:
                        missing_item = olt_client if olt_client is not None else db_client
                        missing_category = "DB" if olt_client is not None else "OLT"
                        log(f"Cliente faltante en {missing_category} : F/S/P/I : {missing_item['fspi']} - SN {missing_item['sn']}", "fail")
                        continue
                    if olt_client['sn'] == db_client['sn']:
                        log(f'CLIENTE : {db_client["contract"]} - {olt_client["fspi"]} | SN DB : {db_client["sn"]} - SN OLT {olt_client["sn"]}',"success")
                    else:
                        log(f'CLIENTE : {db_client["contract"]} - {olt_client["fspi"]} | SN DB : {db_client["sn"]} - SN OLT {olt_client["sn"]}',"warning")
                log(f"No. clientes en db : {len(response)}", "info")
                log(f"No. de clientes en olt : {len(clients)}", "ok")
    quit_ssh()