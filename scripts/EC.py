from time import sleep
from helpers.handlers import request, printer, spid, display, wan_handler
from helpers.finder import optical, last_down_onu
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
optical_values = optical.optical_values
display = display.display
wan_data = wan_handler.wan_data


def client_delete(comm, command, quit_ssh, device, _):
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
    client = req["data"]
    client["olt"] = device
    (client["temp"], client["pwr"], client["pwr_rx"]) = optical_values(comm, command, client, False)
    (
        client["last_down_cause"],
        client["last_down_time"],
        client["last_down_date"],
        client["status"],
    ) = down_values(comm, command, client, False)
    client["spid"] = calculate_spid(client)[
        "I" if "_IP" not in client["plan_name"] else "P"
    ]
    (client["ip"], client["mask"]) = wan_data(comm, command, client)
    proceed = display(client, "A")

    if not proceed:
        log("Cancelando...", "info")
        quit_ssh()
        return

    command(f"undo service-port {client['spid']}")
    log(f"El SPID {client['spid']} ha sido liberado!", "info")
    sleep(3)
    command(f"interface gpon {client['frame']}/{client['slot']}")
    sleep(3)
    command(f"ont delete {client['port']} {client['onu_id']}")
    sleep(3)
    log(
        f'Cliente {client["name_1"]} {client["name_2"]} {client["contract"]} ha sido eliminado',
        "info",
    )

    payload["lookup_type"] = "C"
    payload["lookup_value"] = {"contract":str(client["contract"]), "olt": device}
    req = db_request(endpoints["remove_client"], payload)
    if req["error"]:
        log("an error occurred removing client from db", "fail")
    else:
        log("successfully removed client from db", "success")

    quit_ssh()
    return
