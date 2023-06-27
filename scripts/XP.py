from helpers.handlers import request, printer, spid, port_condition
from helpers.finder import last_down_onu, table
from helpers.constants import definitions, regex_conditions

# FUNCTION IMPORT DEFINITIONS
db_request = request.db_request
inp = printer.inp
log = printer.log
calculate_spid = spid.calculate_spid
endpoints = definitions.endpoints
olt_devices = definitions.olt_devices
payload = definitions.payload
down_values = last_down_onu.down_values
clients_table = table.clients_table
ports = regex_conditions.ports
condition = port_condition.condition


def client_ports(comm, command, quit_ssh, device, action):
    keep = True
    lst = []
    payload["lookup_type"] = action
    payload["lookup_value"] = (
        inp("Ingrese el f/s/p a monitorear : ") if "VP" in action else None
    )
    lst = (
        [{"fsp": payload["lookup_value"]}]
        if "VP" in action
        else ports["olt"][str(device)]
    )

    while keep:
        CLIENTS = []
        req = db_request(endpoints["get_clients"], payload)
        if req["error"]:
            print("an error occurred")
            return

        clients = req["data"]
        client_list = clients_table(comm, command, lst)

        for client in clients:
            for client_lst in client_list:
                if client["fspi"] == client_lst["fspi"]:
                    name = f"{client['name_1']} {client['name_2']} {client['contract']}"
                    client["name"] = name
                    client["pwr"] = client_lst["pwr"]
                    client["last_down_time"] = client_lst["last_down_time"]
                    client["last_down_date"] = client_lst["last_down_date"]
                    client["last_down_cause"] = client_lst["last_down_cause"]
                    CLIENTS.append(client)

        log(
            f"| {'f/s/p':^6} | {'onu_id':^6} | {'name':^54} | {'state':^11} | {'status':^7} | {'last_down_cause':^15} | {'pwr':^6} | {'last_down_time':^14} | {'last_down_date':^14} | {'device':^10} | {'sn':^16} | {'plan':^15} |",
            "normal",
        )

        for clt in CLIENTS:
            alert = condition(clt)
            last_down_time = str(clt["last_down_time"])
            last_down_date = str(clt["last_down_date"])
            last_down_cause = str(clt["last_down_cause"])
            client_row = f"""| {clt['fsp']:^6} | {clt['onu_id']:^6} | {clt["name"]:^54} | {clt['state']:^11} | {clt['status']:^7} | {last_down_cause:^15} | {clt['pwr']:^6} | {last_down_time:^14} | {last_down_date:^14} | {clt['device']:^10} | {clt['sn']:^16} | {clt['plan_name_id']:^15} |"""

            if action in ["VP", "VT"]:
                log(client_row, alert)
            if action == "CA":
                log(client_row, alert) if alert in ["los", "los+"] else None
            if action == "DT":
                log(client_row, alert) if alert in ["suspended", "suspended+"] else None

        preg = inp("continuar? [Y | N] : ") if action == "VP" else None
        payload["lookup_value"] = (
            inp("Ingrese el f/s/p a monitorear : ")
            if action == "VP" and preg == "Y"
            else None
        )
        lst = (
            [{"fsp": payload["lookup_value"]}]
            if action == "VP" and preg == "Y"
            else None
        )
        keep = bool(preg == "Y")
    quit_ssh()
    return
