from time import sleep
from helpers.handlers import request, printer, spid, add_onu, display
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
change_types = definitions.change_types
add_service = add_onu.add_service
optical_values = optical.optical_values
display = display.display


def client_modify(comm, command, quit_ssh, device, _):
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
        client["status"],
    ) = down_values(comm, command, client, False)
    client["spid"] = calculate_spid(client)[
        "I" if "_IP" not in client["plan_name"] else "P"
    ]
    proceed = display(client, "A")

    if not proceed:
        log("Cancelando...", "info")
        quit_ssh()
        return

    # put update types
    change_type = inp(
        """
Que cambio se realizara? 
  > (CT)    :   Cambiar Titular
  > (CO)    :   Cambiar ONT
  > (CP)    :   Cambiar Plan & Proveedor
  > (ES)    :   Eliminar Service Port
  > (AS)    :   Agregar Service Port
$ """
    )
    if change_type not in change_types:
        log("Tipo de modificacion no existe...", "fail")
        quit_ssh()
        return
    payload["change_field"] = change_type
    new_values = {}

    if change_type == "CT":
        new_values["name_1"] = inp("Ingrese el nuevo nombre_1 : ")
        new_values["name_2"] = inp("Ingrese el nuevo nombre_2 : ")
        new_values["contract"] = inp("Ingrese el nuevo contrato : ").zfill(10)
        command(f'interface gpon {client["frame"]}/{client["slot"]}')
        sleep(3)
        command(
            f'ont modify {client["port"]} {client["onu_id"]} desc "{new_values["name_1"]} {new_values["name_2"]} {new_values["contract"]}"'
        )
        sleep(3)

    if change_type == "CP":
        new_values["plan_name"] = inp("Ingrese el nuevo plan a instalar : ")
        db_plans = db_request(endpoints["get_plans"], {})["data"]
        plan_lists = [item["plan_name"] for item in db_plans]

        if new_values["plan_name"] not in plan_lists:
            log("El plan ingresado no existe...", "fail")
            return

        plan = next(
            (item for item in db_plans if item["plan_name"] == new_values["plan_name"]),
            None,
        )

        sleep(3)
        command(f'undo service-port {client["spid"]}')
        sleep(3)
        command(f'interface gpon {client["frame"]}/{client["slot"]}')
        sleep(3)
        command(
            f"ont modify {client['port']} {client['onu_id']} ont-lineprofile-id {plan['line_profile']}"
        )
        sleep(3)
        command(
            f"ont modify {client['port']} {client['onu_id']} ont-srvprofile-id {plan['srv_profile']}"
        )
        sleep(3)
        client["wan"] = [plan]
        client["plan_name"] = new_values["plan_name"]
        add_service(command, client)
        sleep(3)

    if change_type == "CO":
        new_values["sn"] = inp("Ingrese el nuevo serial del cliente : ")
        sleep(3)
        command(f'interface gpon {client["frame"]}/{client["slot"]}')
        sleep(3)
        command(f'ont modify {client["port"]} {client["onu_id"]} sn {new_values["sn"]}')

    if change_type == "ES":
        command(f'undo service-port {client["spid"]}')

    if change_type == "AS":
        client["wan"][0] = plan
        add_service(comm, command, client)

    if change_type not in ["ES", "AS"]:
        payload["new_values"] = new_values
        req = db_request(endpoints["update_client"], payload)
        if req["error"]:
            log("an error occurred updating client from db", "fail")
        else:
            log("successfully updated client from db", "success")
    quit_ssh()
    return
