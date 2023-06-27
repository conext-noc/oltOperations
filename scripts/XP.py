from helpers.handlers import request, printer, spid, port_condition
from helpers.finder import last_down_onu, table
from helpers.constants import definitions, regex_conditions
from helpers.utils import portHandler 

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
vp_count = regex_conditions.vp_count
condition = port_condition.condition
portCounter = portHandler.portCounter
dictToZero = portHandler.dictToZero


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

            portCounter(alert, clt['plan_name_id'])
            vp_count['1']['vp_ttl'] += 1

            if action in ["VP", "VT"]:
                log(client_row, alert)
            if action == "CA":
                log(client_row, alert) if alert in ["los", "los+"] else None
            if action == "DT":
                log(client_row, alert) if alert in ["suspended", "suspended+"] else None
        log(f"""
En el Puerto {clt['fsp']}:
El total de clientes en el puerto es           :   {vp_count['1']['vp_ttl']}
El total de clientes activos es                :   {vp_count['1']['vp_active_cnt']}
El total de clientes desactivados es           :   {vp_count['1']['vp_deactive_cnt']}
El total de clientes activos en corte es       :   {vp_count['1']['vp_los_cnt']}
El total de clientes activos apagados es       :   {vp_count['1']['vp_off_cnt']}

Proveedores :
El total de clientes con VNET es           :   {vp_count['2']['vp_vnet']}
El total de clientes con INTER es          :   {vp_count['2']['vp_inter']}
El total de clientes con IP PÚBLICA es     :   {vp_count['2']['vp_public_ip']}

Planes :
El total de clientes con Plan FAMILY        :   {vp_count['2']['OZ_0']}
El total de clientes con Plan MAX           :   {vp_count['2']['OZ_MAX']}
El total de clientes con Plan SKY           :   {vp_count['2']['OZ_SKY']}
El total de clientes con Plan MAGICAL       :   {vp_count['2']['OZ_MAGICAL']}
El total de clientes con Plan NEXT          :   {vp_count['2']['OZ_NEXT']}
El total de clientes con Plan PLUS          :   {vp_count['2']['OZ_PLUS']}
El total de clientes con Planes DEDICADOS   :   {vp_count['2']['OZ_DEDICADO']}
El total de clientes con Plan CONECTA       :   {vp_count['2']['OZ_CONECTA']}
El total de Clientes sin Plan Asignado      :   {vp_count['2']['NA']}
""", "normal")if action in ["VP", "VT"] else None
        dictToZero(vp_count['1'])
        dictToZero(vp_count['2'])
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
