from helpers.handlers import request, printer, spid, display, template
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
approvedDis = template.approvedDis


def client_lookup(comm, command, quit_ssh, device, _):
    payload["lookup_type"] = inp(
        "Buscar cliente por Contrato, Serial o Datos [C | S | D] : "
    )
    payload["lookup_value"] = inp("Ingrese el contrato, serial o datos (f/s/p/id) : ")
    req = db_request(endpoints["get_client"], payload)
    if req["error"]:
        log(req["message"], "fail")
        quit_ssh()
        return
    client = req["data"]
    client["olt"] = device
    (client["temp"], client["pwr"]) = optical_values(comm, command, client, False)
    (
        client["last_down_cause"],
        client["last_down_time"],
        client["last_down_date"],
    ) = down_values(comm, command, client, False)
    client["spid"] = calculate_spid(client)[
        "I" if "_IP" not in client["plan_name"] else "P"
    ]
    display(client, "B")
    displayTemplate = (
        inp("Desea la plantilla de datos operacionales? [Y/N] : ").upper().strip()
        == "Y"
    )
    approvedDis(client) if displayTemplate else None
    return
