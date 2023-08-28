from time import sleep
from helpers.constants.definitions import endpoints, payload
from helpers.utils.decoder import check_iter, decoder
from helpers.handlers.request import db_request
from helpers.handlers.fail import fail_checker
from helpers.handlers.printer import log
from helpers.handlers.file_formatter import data_to_dict
from helpers.utils.ssh import ssh


def clientsTable(comm, command, fsp):
    CLIENTS = []
    FRAME = int(fsp.split("/")[0])
    SLOT = int(fsp.split("/")[1])
    PORT = int(fsp.split("/")[2])
    command(f"display ont info {FRAME} {SLOT} {PORT} all  | no-more")
    sleep(3)
    value = decoder(comm)
    fail = fail_checker(value)
    if fail != None:
        log(fail, "fail")
        return []
    rePort = check_iter(value, "-----------------------------------------------------------------------------")
    header = "F/,S/P,ID,SN,state,status,conf,match,prot," if SLOT < 10 else "F/S/P,ID,SN,state,status,conf,match,prot,"
    body = value[rePort[1][1]:rePort[2][0]]
    valueStatePort = data_to_dict(header, body)
    for client in valueStatePort:
        CLIENTS.append({
          "fspi": f"{client['F/']}{client['S/P']}/{client['ID']}" if SLOT < 10 else f"{client['F/S/P']}/{client['ID']}",
          "olt": 1,
          "state": client["state"]
        })
    log(f"{fsp} done", "success")
    return CLIENTS

def db_sync(comm,command, quit_ssh, olt, action):
    _ = decoder(comm)
    for slot in range(1,16):
        if slot == 8 or slot == 9:
            continue
        else:
            for port in range(0,16):
                clients = clientsTable(comm, command, f"0/{slot}/{port}")
                for client in clients:
                    payload["lookup_type"] = "D"
                    payload["lookup_value"] = client["fspi"]
                    payload["new_values"] = {"state": client["state"]}
                    payload["change_field"] = "OX"
                    response = db_request(endpoints["update_client"], payload)
                    log(f'{response["message"]} - {response["data"]["contract"]} - {client["fspi"]}',"success") if not response["error"] else log(f'{response["message"]} - {client["fspi"]}',"fail")
    quit_ssh()