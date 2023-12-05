from helpers.handlers import request, printer, spid, display, template, wan_handler
from helpers.finder import optical, last_down_onu
from helpers.constants import definitions
from helpers.handlers.enable_wan_handler import enable_wan

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
approvedDis = template.approvedDis
wan_data = wan_handler.wan_data


def client_lookup(comm, command, quit_ssh, device, _):
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
    (client["temp"], client["pwr"], client["pwr_rx"]) = optical_values(
        comm, command, client, False
    )
    (
        client["last_down_cause"],
        client["last_down_time"],
        client["last_down_date"],
        client["status"],
    ) = down_values(comm, command, client, False)
    provider = (
        "INTER"
        if "_1" in client["plan_name"]
        else "VNET"
        if "_2" in client["plan_name"]
        else "IP"
    )
    client["provider"] = provider
    client["spid"] = calculate_spid(client)[
        "I" if "_IP" not in client["plan_name"] else "P"
    ]
    (client["ip"], client["mask"]) = wan_data(comm, command, client)
    display(client, "B")
    enable_wan(command, client)
    displayTemplate = (
        inp("Desea la plantilla de datos operacionales? [Y/N] : ").upper().strip()
        == "Y"
    )
    approvedDis(client) if displayTemplate else None
    return
