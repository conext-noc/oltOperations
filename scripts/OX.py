from tkinter import filedialog
from helpers.handlers import request, printer, spid, file_formatter
from helpers.finder import last_down_onu
from helpers.constants import definitions

# FUNCTION IMPORT DEFINITIONS
db_request = request.db_request
inp = printer.inp
log = printer.log
calculate_spid = spid.calculate_spid
endpoints = definitions.endpoints
olt_devices = definitions.olt_devices
payload = definitions.payload
down_values = last_down_onu.down_values
file_to_dict = file_formatter.file_to_dict


def client_operate(_, command, quit_ssh, __, action):
    clients = []
    if "U" in action:
        payload["lookup_type"] = inp("Buscar cliente por Contrato, Serial o Datos [C | S | D] : ")
        payload["lookup_value"] = inp("enter value : ")
        req = db_request(endpoints["get_client"], payload)
        if req["error"]:
            log(req["message"], "fail")
            quit_ssh()
            return

        clients = [req["data"]]
    if "L" in action:
        file_name = filedialog.askopenfilename()
        file_type = inp("Es un archivo CSV o EXCEL? [C : E]: ")
        action_list = file_to_dict(file_name, file_type)

        for client in action_list:
            payload["lookup_type"] = "C"
            payload["lookup_value"] = client["contract"]
            req = db_request(endpoints["get_client"], payload)
            clients.append(req["data"])

    operation = "activate" if "R" in action else "deactivate"
    resulted_operation = "active" if "R" in action else "deactivated"
    result = "Reactivado" if "R" in action else "Suspendido"

    for client in clients:
        command(f'interface gpon {client["frame"]}/{client["slot"]}')
        command(f'ont {operation} {client["port"]}/{client["onu_id"]}')

        payload["change_field"] = "OX"
        payload["new_values"] = resulted_operation
        req = db_request(endpoints["update_client"], payload)

        log(
            f'Cliente {client["name_1"]} {client["name_2"]} {client["contract"]} ha sido {result}',
            "info",
        )
    return
