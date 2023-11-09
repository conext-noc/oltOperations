from helpers.handlers import request, printer, spid, add_onu, template, display
from helpers.finder import optical, last_down_onu, device_type, new_onu
from helpers.constants import definitions

# FUNCTION IMPORT DEFINITIONS
db_request = request.db_request
add_service = add_onu.add_service
add_client = add_onu.add_client
optical_values = optical.optical_values
new_lookup = new_onu.new_lookup
inp = printer.inp
log = printer.log
calculate_spid = spid.calculate_spid
endpoints = definitions.endpoints
payload_add = definitions.payload_add
down_values = last_down_onu.down_values
client_place_holder = definitions.client_place_holder
client_payload = definitions.client_payload
type_finder = device_type.type_finder
approved = template.approved
denied = template.denied
display = display.display
approvedDis = template.approvedDis



def client_install(comm, command, quit_ssh, device, _):
    
    client = client_place_holder.copy()
    NEW_SN = inp("Ingrese el Serial del Cliente a buscar : ").upper()
    (client["sn"], client["fsp"]) = new_lookup(comm, command, NEW_SN)
    val = inp("desea continuar? [Y|N] : ").upper()
    proceed = bool(val == "Y" and client["sn"] is not None)

    if not proceed:
        log("SN no aparece en OLT, Saliendo...", "warning")
        quit_ssh()
        return
    client["frame"] = int(client["fsp"].split("/")[0])
    client["slot"] = int(client["fsp"].split("/")[1])
    client["port"] = int(client["fsp"].split("/")[2])

    client["plan_name"] = inp("Ingrese plan del cliente : ")

    db_plans = db_request(endpoints["get_plans"],{})["data"]
    plan_lists = [item["plan_name"] for item in db_plans]

    if client["plan_name"] not in plan_lists:
        log("El plan ingresado no existe...", "fail")
        return

    plan = next(
        (item for item in db_plans if item["plan_name"] == client["plan_name"]),
        None,
    )

    client["line_profile"] = plan["line_profile"]
    client["srv_profile"] = plan["srv_profile"]
    client["wan"][0] = plan

    client["name_1"] = inp(
        "Ingrese Primer nombre del cliente, nombre de empresa o residencia-condominio : "
    ).replace(" ", "_")
    client["name_2"] = inp(
        "Ingrese Segundo nombre del cliente, ca o nombre de residencia-condominio : "
    ).replace(" ", "_")
    client["contract"] = inp("Ingrese contrato del cliente : ")[:10].zfill(10)

    while len(f'{client["name_1"]} {client["name_2"]} {client["contract"]}') > 56:
        log("nombre total excede los 56 caracteres maximos permitidos ... intente nuevamente", "warning")
        client["name_1"] = inp(
            "Ingrese Primer nombre del cliente, nombre de empresa o residencia-condominio : "
        ).replace(" ", "_")
        client["name_2"] = inp(
            "Ingrese Segundo nombre del cliente, ca o nombre de residencia-condominio : "
        ).replace(" ", "_")
        client["contract"] = inp("Ingrese contrato del cliente : ")[:10].zfill(10)

    (client["onu_id"], client["fail"]) = add_client(comm, command, client)
    (client["temp"], client["pwr"], client["pwr_rx"]) = optical_values(comm, command, client, True)

    value = inp(
        f"""
La potencia de Recepcion del OLT : {client["pwr_rx"]}
La potencia de Recepcion del ONT : {client["pwr"]}
La temperatura es : {client["temp"]}
quieres proceder con la instalacion? [Y | N] : """
    )
    install = True if value == "Y" else False if value == "N" else None

    if not install:
        reason = inp("Por que no se le asignara servicio? : ").upper()
        denied(client, reason)
        command(f'interface gpon {client["frame"]} {client["slot"]}')
        command(f'ont delete {client["port"]} {client["onu_id"]}')
        log("Cliente no se agrego apropiadamente en OLT, eliminando...", "warning")

        (client["device"], client["vendor"]) = type_finder(comm, command, client)
        if client["vendor"] == "BDCM":
            client['device'] = client['vendor']
        # log(f"El tipo de ONT del cliente es {client['device']}", "ok")
        
        client['status'] = "offline"
        client['state'] = "deactivate"

        for key in client_payload:
            client_payload[key] = client[key]

        client_payload["olt"] = device
        client_payload["fsp"] = f'{client["frame"]}/{client["slot"]}/{client["port"]}'
        client_payload[
            "fspi"
        ] = f'{client["frame"]}/{client["slot"]}/{client["port"]}/{client["onu_id"]}'
        client_payload["spid"] = 0
        client_payload["device"] = client["device"]
        payload_add["data"] = client_payload.copy()
        req = db_request(endpoints["add_client"], payload_add)
        if req["error"]:
            # print(req["message"])
            # print(payload_add["data"])
            log("an error occurred adding to db", "fail")
        else:
            log("successfully added client to db", "success")
        quit_ssh()
        return

    (client["device"], client["vendor"]) = type_finder(comm, command, client)
    if client["vendor"] == "BDCM":
        client['device'] = client['vendor']
    log(f"El tipo de ONT del cliente es {client['device']}", "ok")

    add_service(command, client)
    
    client['status'] = "online"
    client['state'] = "active"

    for key in client_payload:
        client_payload[key] = client[key]

    client_payload["olt"] = device
    client_payload["fsp"] = f'{client["frame"]}/{client["slot"]}/{client["port"]}'
    client_payload[
        "fspi"
    ] = f'{client["frame"]}/{client["slot"]}/{client["port"]}/{client["onu_id"]}'
    client_payload["spid"] = client["wan"][0]["spid"]
    payload_add["data"] = client_payload.copy()
    req = db_request(endpoints["add_client"], payload_add)
    if req["error"]:
        log("an error occurred adding to db", "fail")
    else:
        log("successfully added client to db", "success")

    client['olt'] = device
    client['provider'] = client["wan"][0]["provider"]
    client['spid'] = client["wan"][0]["spid"]
    client['vlan'] = client["wan"][0]["vlan"]
    approved(client)
    display(client, "B")
    displayTemplate = (
        inp("Desea la plantilla de datos operacionales? [Y/N] : ").upper().strip()
        == "Y"
    )
    approvedDis(client) if displayTemplate else None
    quit_ssh()
    return
