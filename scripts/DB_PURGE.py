from dotenv import load_dotenv
from helpers.handlers.request import db_request
from helpers.constants.definitions import (
    olt_devices,
    snmp_oid,
    endpoints,
    snmp_down_causes,
    snmp_state_types,
    snmp_status_types,
)
from helpers.handlers.hex_string import hex_to_string
from helpers.utils.snmp import SNMPBulk, SNMPNext
from helpers.handlers.file_formatter import dict_to_file
from helpers.handlers.printer import inp, log

load_dotenv()


def db_purge(comm, command, quit_ssh, olt, action):
    ports = db_request(endpoints["get_ports"], {})["data"]
    open_ports = [port for port in ports if port.get('is_open') and int(port.get('olt')) == int(olt)]
    open_ports_sorted = sorted(open_ports, key=lambda x: x.get('port_id', 0))
    last_known_port_id = int(inp("ingrese el ultimo id de puerto utilizado : "))
    for port in open_ports_sorted:
        if int(port["port_id"]) >= last_known_port_id:
            log(f"requesting clients via snmp on port id {port['port_id']} `{port['fspo']}`","info")
            clients = []
            snmp_next = SNMPNext(olt_devices[olt], f'{snmp_oid["descr"]}.{port["oid"]}')
            values = snmp_next.execute()
            ont_ids = []
            for value in values:
                ont_ids.append(
                    ""
                    if value.prettyPrint().split(" = ")[0].split(".")[-1] == "0"
                    else value.prettyPrint().split(" = ")[0].split(".")[-1]
                )
            for ont_id in ont_ids:
                snmp = SNMPBulk(
                    olt_devices[str(1)],
                    f'{snmp_oid["descr"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["serial"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["power"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["ldc"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["lddt"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["status"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["device"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["ip_addr"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["state"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["srv_prof"]}.{port["oid"]}.{ont_id}',
                    f'{snmp_oid["lin_prof"]}.{port["oid"]}.{ont_id}',
                )
                data = snmp.execute()
                if len(data) == 0:
                    log(f"missing client @ port : {port['port_id']} `{port['fspo']}`, adding to file : missing.txt","warning")
                    print(f"{port['fspo']} | ont {ont_id}", file=open("missing.txt", "a"))
                    continue
                desc = data[0].prettyPrint().split(" = ")[-1]
                client = {
                    "name_1": desc.split(" ")[0],
                    "name_2": desc.split(" ")[1] if len(desc.split(" ")) > 1 else "",
                    "contract": desc.split(" ")[-1],
                    "frame": port["frame"],
                    "slot": port["slot"],
                    "port": port["port"],
                    "onu_id": 0 if ont_id == "" else ont_id,
                    "sn":data[1].prettyPrint().split(" = ")[-1],
                    "power":f"{int(data[2].prettyPrint().split(' = ')[-1])/100:.2f}",
                    "last_down_cause": snmp_down_causes[data[3].prettyPrint().split(" = ")[-1]],
                    "last_down_time": hex_to_string(data[4].prettyPrint().split(" = ")[-1])[1],
                    "last_down_date": hex_to_string(data[4].prettyPrint().split(" = ")[-1])[0],
                    "status": snmp_status_types[data[5].prettyPrint().split(" = ")[-1]],
                    "device": data[6].prettyPrint().split(" = ")[-1],
                    "ip": data[7].prettyPrint().split(" = ")[-1],
                    "state": snmp_state_types[data[8].prettyPrint().split(" = ")[-1]],
                    "srv_prof": data[9].prettyPrint().split(" = ")[-1],
                    "line_prof": data[10].prettyPrint().split(" = ")[-1],
                }
                clients.append(client)
            file_name = f'{port["frame"]}-{port["slot"]}-{port["port"]}-{port["olt"]}_purge_db'
            log(f"done requesting clients via snmp on port id {port['port_id']} `{port['fspo']}`, generating file : {file_name}.csv","success")
            dict_to_file(fileName=file_name, fileType="C", path="./", data=clients, show=False)
