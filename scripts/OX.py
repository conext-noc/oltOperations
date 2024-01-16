from tkinter import filedialog
from helpers.handlers import request, printer, spid, file_formatter
from helpers.finder import last_down_onu
from helpers.constants import definitions
from helpers.constants.snmp_data import map_ports,SNMP_OIDS
from helpers.utils.snmp import SNMP_set
from dotenv import load_dotenv
import os

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

load_dotenv()

def client_operate(_, command, quit_ssh, device, action):
    clients = []
    if "U" in action:
        payload["lookup_type"] = inp(
            "Buscar cliente por Contrato, Serial o Datos [C | S | D] : "
        )
        value = inp("Ingrese el contrato, serial o datos (f/s/p/id) : ")

        value = value.zfill(10) if payload["lookup_type"] == "C" else value
        value_class = (
            "contract"
            if payload["lookup_type"] == "C"
            else "fspi"
            if payload["lookup_type"] == "D"
            else "serial"
        )

        payload["lookup_value"] = {"olt": device, f"{value_class}": value}
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
            payload["lookup_value"] = {"contract": client["contract"], "olt": client["olt"]}
            req = db_request(endpoints["get_client"], payload)
            clients.append(req["data"])

    # operation = "activate" if "R" in action else "deactivate"
    operation = '1' if "R" in action else '2'
    resulted_operation = "active" if "R" in action else "deactivated"
    result = "Reactivado" if "R" in action else "Suspendido"

    list_len = len(clients)

    for curr, client in enumerate(clients):
        fsp = f"{client['frame']}/{client['slot']}/{client['port']}"

        for fsp_oid,value in map_ports.items():
            if value == fsp:
                olt = client["olt"]
                SNMP_set(os.environ["SNMP_WRITE"],olt_devices[str(olt)],SNMP_OIDS["STATE"],161,fsp_oid,client["onu_id"],operation)

        payload["change_field"] = "OX"
        payload["new_values"] = {"state": resulted_operation}
        req = db_request(endpoints["update_client"], payload)

        log(
            f'{curr + 1} | Cliente {client["name_1"]} {client["name_2"]} {client["contract"]} ha sido {result} | progreso {(curr+1)*100/list_len}%',
            "info",
        )
    return
