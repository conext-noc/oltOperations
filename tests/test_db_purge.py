import os
import sys
import unittest
from pysnmp.hlapi import (
    CommunityData,
    ContextData,
    ObjectType,
    ObjectIdentity,
    UdpTransportTarget,
    bulkCmd,
    SnmpEngine,
    nextCmd,
)
from dotenv import load_dotenv

load_dotenv()

current_directory = os.getcwd()
sys.path.append(current_directory)

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


class TestSnmpBulkCompiler(unittest.TestCase):
    def test_snmp_bulk(self):
        ports = db_request(endpoints["get_ports"], {})["data"]
        clients = []
        for port in ports:
            snmp_next = SNMPNext(
                olt_devices[str(1)], f'{snmp_oid["descr"]}.{port["oid"]}'
            )
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
                            f'{ snmp_oid["lddt"]}.{port["oid"]}.{ont_id}',
                            f'{ snmp_oid["status"]}.{port["oid"]}.{ont_id}',
                            f'{ snmp_oid["device"]}.{port["oid"]}.{ont_id}',
                            f'{ snmp_oid["ip_addr"]}.{port["oid"]}.{ont_id}',
                            f'{ snmp_oid["state"]}.{port["oid"]}.{ont_id}',
                            f'{ snmp_oid["srv_prof"]}.{port["oid"]}.{ont_id}',
                            f'{ snmp_oid["lin_prof"]}.{port["oid"]}.{ont_id}',
                        )
                data = snmp.execute()
                desc = data[0].prettyPrint().split(" = ")[-1]
                client = {
                    "name_1":desc.split(" ")[0],
                    "name_2":desc.split(" ")[1] if len(desc.split(" ")) > 1 else "",
                    "contract":desc.split(" ")[-1],
                    "frame":port["frame"],
                    "slot":port["slot"],
                    "port": port["port"],
                    "onu_id": 0 if ont_id == "" else ont_id,
                    "sn":data[1].prettyPrint().split(" = ")[-1],
                    "power":f"{int(data[2].prettyPrint().split(' = ')[-1])/100:.2f}",
                    "last_down_cause":snmp_down_causes[data[3].prettyPrint().split(" = ")[-1]],
                    "last_down_time":hex_to_string(data[4].prettyPrint().split(" = ")[-1])[1],
                    "last_down_date":hex_to_string(data[4].prettyPrint().split(" = ")[-1])[0],
                    "status":snmp_status_types[data[5].prettyPrint().split(" = ")[-1]],
                    "device":data[6].prettyPrint().split(" = ")[-1],
                    "ip":data[7].prettyPrint().split(" = ")[-1],
                    "state":snmp_state_types[data[8].prettyPrint().split(" = ")[-1]],
                    "srv_prof":data[9].prettyPrint().split(" = ")[-1],
                    "line_prof":data[10].prettyPrint().split(" = ")[-1],
                }
                clients.append(client)
        pass


if __name__ == "__main__":
    unittest.main()
