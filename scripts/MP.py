from time import sleep
from helpers.handlers.add_onu import add_service_mp
from helpers.handlers.enable_wan_handler import enable_wan
from helpers.handlers.printer import inp, log
from helpers.handlers.request import db_request
from helpers.constants.definitions import endpoints, payload, bridges
from helpers.handlers.spid import calculate_spid

def print_client(client):
    print(
        f"""
NOMBRE          :       {client['name_1']} {client['name_2']}
CONTRATO        :       {client["contract"]}
FSPI            :       {client["fspi"]}
PLAN            :       {client["plan_name_id"]}
INDEX DE PLAN   :       {client["plan_idx"]}
SRV PROFILE     :       {client["srv_profile"]}
LINE PROFILE    :       {client["line_profile"]}
GEM PORT        :       {client["gem_port"]}
VLAN            :       {client["vlan"]}
SPID            :       {client["spid"]}
VENDOR          :       {client["device"] or None}
"""
    )

def data_plan_migration(comm,command, quit_ssh, device, _):
    ports = db_request(endpoints["get_ports"], {})["data"]
    data_plans = db_request(endpoints["get_plans"], {})["data"]
    all_plans = [plan["plan_name"] for plan in data_plans]

    OLD_PLAN = inp("Ingrese el plan a remplazar :   ")
    while OLD_PLAN not in all_plans:
        log(f"el plan {OLD_PLAN} no existe en la base de datos ... intente nuevamente", "warning")
        OLD_PLAN = inp("Ingrese el plan a remplazar :   ")
    NEW_PLAN = inp("Ingrese el nuevo plan       :   ")
    while NEW_PLAN not in all_plans:
        log(f"el plan {NEW_PLAN} no existe en la base de datos ... intente nuevamente", "warning")
        NEW_PLAN = inp("Ingrese el nuevo plan       :   ")

    for port_data in ports:
        if device == str(port_data["olt"]) and port_data["is_open"]:
            payload["lookup_type"] = "VP"
            payload["lookup_value"] = {"fsp":f'{port_data["frame"]}/{port_data["slot"]}/{port_data["port"]}', "olt": device}
            clients_req = db_request(endpoints["get_clients"], payload).get("data")
            for client_req in clients_req:
                if OLD_PLAN == client_req["plan_name_id"]:
                    data_plan_req = [
                        data_plan
                        for data_plan in data_plans
                        if client_req["plan_name_id"] == data_plan["plan_name"]
                    ][0]
                    spid_data = calculate_spid(client_req)
                    spid = (
                        spid_data["I"]
                        if "IP" in client_req["plan_name_id"]
                        else spid_data["P"]
                    )
                    client = client_req.copy()

                    new_plan = [
                        data_plan
                        for data_plan in data_plans
                        if NEW_PLAN == data_plan["plan_name"]
                    ][0]
                    client.update(data_plan_req)
                    client["spid"] = spid
                    print_client(client)
                    command(f'undo service-port {client["spid"]}')
                    command(f'interface gpon {client["frame"]}/{client["slot"]}')
                    command(
                        f"ont modify {client['port']} {client['onu_id']} ont-lineprofile-id {new_plan['line_profile']}"
                    )
                    command(
                        f"ont modify {client['port']} {client['onu_id']} ont-srvprofile-id {new_plan['srv_profile']}"
                    )
                    add_service_mp(command, client, new_plan)
                    if client["device"] in bridges:
                        command(f'interface gpon {client["frame"]}/{client["slot"]}')
                        command(f"ont reset {client['port']} {client['onu_id']}")
                        command('quit')
                    enable_wan(command, client, True)
                    payload_new = {"type": "a","change_field": "CP","lookup_type":"C","lookup_value":{ "contract":client['contract'],"olt": device},"new_values": {"plan_name": new_plan["plan_name"]}}
                    req = db_request(endpoints["update_client"], payload_new)
                    if req["error"]:
                        log("an error occurred updating client from db", "fail")
                    else:
                        log("successfully updated client from db", "success")

    quit_ssh()
    return